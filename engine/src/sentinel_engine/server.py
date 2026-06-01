from __future__ import annotations

import asyncio
import contextlib
import queue
import sys
import threading
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from sentinel_engine.capture import FrameSource
from sentinel_engine.controller import EngineController
from sentinel_engine.types import Frame


def _offer(
    loop: asyncio.AbstractEventLoop,
    outbox: asyncio.Queue[dict[str, Any]],
    item: dict[str, Any],
) -> None:
    def put() -> None:
        with contextlib.suppress(asyncio.QueueFull):
            outbox.put_nowait(item)

    loop.call_soon_threadsafe(put)


def _replace_latest(slot: queue.Queue[Frame], frame: Frame) -> None:
    with contextlib.suppress(queue.Empty):
        slot.get_nowait()
    with contextlib.suppress(queue.Full):
        slot.put_nowait(frame)


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
        display_done = threading.Event()
        latest: queue.Queue[Frame] = queue.Queue(maxsize=1)

        def capture_loop() -> None:
            frames: Iterator[Frame] = source.frames()
            try:
                for frame in frames:
                    if stop.is_set():
                        break
                    try:
                        _offer(
                            loop, outbox, controller.frame_event(frame).model_dump()
                        )
                    except Exception as error:
                        print(
                            f"frame {frame.id} display failed: {error}",
                            file=sys.stderr,
                        )
                    _replace_latest(latest, frame)
            finally:
                close = getattr(frames, "close", None)
                if callable(close):
                    close()
                display_done.set()

        def analysis_loop() -> None:
            while not stop.is_set():
                try:
                    frame = latest.get(timeout=0.1)
                except queue.Empty:
                    if display_done.is_set():
                        break
                    continue
                try:
                    event = controller.process_frame(frame)
                    if event is None:
                        continue
                    _offer(loop, outbox, event.model_dump())
                    _offer(loop, outbox, controller.metrics().model_dump())
                except Exception as error:
                    print(f"frame {frame.id} analysis failed: {error}", file=sys.stderr)

        workers = [
            threading.Thread(target=capture_loop, daemon=True),
            threading.Thread(target=analysis_loop, daemon=True),
        ]
        for worker in workers:
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

    from sentinel_engine.capture import LatestFrameCamera
    from sentinel_engine.config import Settings
    from sentinel_engine.controller import build_controller
    from sentinel_engine.embed import FastEmbedImageEmbedder
    from sentinel_engine.session import SessionLog
    from sentinel_engine.tuner import detect_profile, tune

    plan = tune(detect_profile())
    print("auto-tuned for this device (Qdrant Skills-style):")
    for choice in plan.choices:
        print(f"  {choice.setting} = {choice.value}  — {choice.rationale}")

    settings = Settings(skip_hamming=plan.skip_hamming, quantize=plan.quantize)
    embedder = FastEmbedImageEmbedder(settings.model_name, settings.cache_dir)
    session = SessionLog(Path("sessions") / "session.jsonl")
    controller = build_controller(settings, embedder, session=session)
    app = create_app(lambda: controller, lambda: LatestFrameCamera())
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run()
