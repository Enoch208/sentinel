from __future__ import annotations

from fastapi.testclient import TestClient
from support import FakeEmbedder

from sentinel_engine.capture import SyntheticScene
from sentinel_engine.config import Settings
from sentinel_engine.controller import build_controller
from sentinel_engine.server import create_app


def test_ws_streams_verdicts_flags_and_acks_commands() -> None:
    controller = build_controller(
        Settings(warmup_frames=8, skip_hamming=0), FakeEmbedder(), in_memory=True
    )
    app = create_app(
        lambda: controller,
        lambda: SyntheticScene(total=40, anomaly_at=(24, 25, 26)),
    )
    client = TestClient(app)

    with client.websocket_connect("/ws") as socket:
        socket.send_json({"type": "sensitivity", "value": 0.8})
        verdicts = 0
        acks = 0
        frames = 0
        for _ in range(160):
            message = socket.receive_json()
            kind = message["type"]
            if kind == "verdict":
                verdicts += 1
            elif kind == "frame":
                frames += 1
                assert len(message["jpeg"]) > 0
            elif kind == "ack":
                acks += 1
            if frames >= 5 and verdicts >= 1 and acks >= 1:
                break

    assert frames >= 5
    assert verdicts >= 1
    assert acks >= 1
