from __future__ import annotations

from support import FakeEmbedder

from sentinel_engine.capture import SyntheticScene
from sentinel_engine.config import Settings
from sentinel_engine.controller import EngineController, build_controller
from sentinel_engine.protocol import AckEvent, TwinsEvent


def _controller() -> EngineController:
    return build_controller(
        Settings(warmup_frames=8, skip_hamming=0), FakeEmbedder(), in_memory=True
    )


def _run(controller: EngineController, total: int = 40) -> None:
    for frame in SyntheticScene(total=total, anomaly_at=(24, 25, 26)).frames():
        controller.process_frame(frame)


def test_process_flags_and_reports_metrics() -> None:
    controller = _controller()
    events = []
    for frame in SyntheticScene(total=40, anomaly_at=(24, 25, 26)).frames():
        event = controller.process_frame(frame)
        if event is not None:
            events.append(event)

    assert any(event.flagged for event in events)
    metric = controller.metrics()
    assert metric.point_count > 0
    assert metric.fps >= 0.0


def test_frame_event_carries_jpeg() -> None:
    controller = _controller()
    frame = next(SyntheticScene(total=1, anomaly_at=()).frames())
    event = controller.frame_event(frame)
    assert event.type == "frame"
    assert event.frame_id == frame.id
    assert len(event.jpeg) > 0


def test_sensitivity_command_acks() -> None:
    controller = _controller()
    ack = controller.handle_command({"type": "sensitivity", "value": 0.9})
    assert isinstance(ack, AckEvent)
    assert ack.ok is True


def test_teach_command_applies_to_recent_frame() -> None:
    controller = _controller()
    _run(controller)
    ack = controller.handle_command(
        {"type": "teach", "frame_id": 24, "label": "expected"}
    )
    assert isinstance(ack, AckEvent)
    assert ack.ok is True


def test_twins_command_returns_twins_event() -> None:
    controller = _controller()
    _run(controller)
    event = controller.handle_command({"type": "twins", "frame_id": 10, "k": 3})
    assert isinstance(event, TwinsEvent)
    assert len(event.results) <= 3


def test_invalid_command_acks_false() -> None:
    controller = _controller()
    ack = controller.handle_command({"type": "bogus"})
    assert isinstance(ack, AckEvent)
    assert ack.ok is False


def test_reset_command_clears_memory() -> None:
    controller = _controller()
    _run(controller)
    controller.handle_command({"type": "reset"})
    assert controller.metrics().point_count == 0
