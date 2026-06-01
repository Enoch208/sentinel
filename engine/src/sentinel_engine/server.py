from __future__ import annotations

import asyncio
import contextlib
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from sentinel_engine.capture import FrameSource
from sentinel_engine.controller import EngineController


def _offer(
    loop: asyncio.AbstractEventLoop,
    outbox: asyncio.Queue[dict[str, Any]],
    item: dict[str, Any],
) -> None:
    def put() -> None:
        with contextlib.suppress(asyncio.QueueFull):
            outbox.put_nowait(item)

    loop.call_soon_threadsafe(put)


def create_app(
    controller_factory: Callable[[], EngineController],
    source_factory: Callable[[], FrameSource],
) -> FastAPI:
    app = FastAPI()

    @app.websocket("/ws")
    async def stream(socket: WebSocket) -> None:
        await socket.accept()
        controller = controller_factory()
        source = source_factory()
        loop = asyncio.get_running_loop()
        outbox: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=256)
        stop = threading.Event()

        def produce() -> None:
            for frame in source.frames():
                if stop.is_set():
                    return
                event = controller.process_frame(frame)
                if event is None:
                    continue
                _offer(loop, outbox, controller.frame_event(frame).model_dump())
                _offer(loop, outbox, event.model_dump())
                _offer(loop, outbox, controller.metrics().model_dump())

        worker = threading.Thread(target=produce, daemon=True)
        worker.start()

        async def send_events() -> None:
            while True:
                item = await outbox.get()
                await socket.send_json(item)

        async def receive_commands() -> None:
            while True:
                raw = await socket.receive_json()
                response = controller.handle_command(raw)
                await socket.send_json(response.model_dump())

        tasks = [
            asyncio.create_task(send_events()),
            asyncio.create_task(receive_commands()),
        ]
        try:
            await asyncio.gather(*tasks)
        except WebSocketDisconnect:
            pass
        finally:
            stop.set()
            for task in tasks:
                task.cancel()

    return app


def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    import uvicorn

    from sentinel_engine.capture import OpenCVCamera
    from sentinel_engine.config import Settings
    from sentinel_engine.controller import build_controller
    from sentinel_engine.embed import FastEmbedImageEmbedder
    from sentinel_engine.session import SessionLog

    settings = Settings()
    embedder = FastEmbedImageEmbedder(settings.model_name, settings.cache_dir)
    session = SessionLog(Path("sessions") / "session.jsonl")
    controller = build_controller(settings, embedder, session=session)
    app = create_app(lambda: controller, lambda: OpenCVCamera())
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run()
