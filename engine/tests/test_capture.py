from __future__ import annotations

import cv2
import numpy as np
import pytest

from sentinel_engine.capture import OpenCVCamera, SyntheticScene


class _FakeCapture:
    def __init__(self, frames: list[np.ndarray]) -> None:
        self._frames = frames
        self._index = 0
        self.released = False

    def isOpened(self) -> bool:
        return True

    def read(self) -> tuple[bool, np.ndarray | None]:
        if self._index < len(self._frames):
            frame = self._frames[self._index]
            self._index += 1
            return True, frame
        return False, None

    def release(self) -> None:
        self.released = True


class _ClosedCapture:
    def isOpened(self) -> bool:
        return False

    def read(self) -> tuple[bool, None]:
        return False, None

    def release(self) -> None:
        return None


def test_yields_requested_frame_count_with_sequential_ids() -> None:
    scene = SyntheticScene(total=10, anomaly_at=(5,))
    frames = list(scene.frames())
    assert len(frames) == 10
    assert [f.id for f in frames] == list(range(10))


def test_anomaly_frame_differs_far_more_than_normal_jitter() -> None:
    scene = SyntheticScene(total=10, anomaly_at=(5,))
    images = {f.id: f.image.astype(np.int32) for f in scene.frames()}

    normal_jitter = np.abs(images[4] - images[3]).mean()
    anomaly_delta = np.abs(images[5] - images[4]).mean()
    assert anomaly_delta > normal_jitter * 5


def test_opencv_camera_yields_frames_until_read_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    frames = [np.zeros((4, 4, 3), dtype=np.uint8) for _ in range(3)]
    capture = _FakeCapture(frames)
    monkeypatch.setattr(cv2, "VideoCapture", lambda index: capture)

    produced = list(OpenCVCamera(0).frames())

    assert [frame.id for frame in produced] == [0, 1, 2]
    assert produced[0].image.shape == (4, 4, 3)
    assert capture.released is True


def test_opencv_camera_raises_when_camera_will_not_open(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(cv2, "VideoCapture", lambda index: _ClosedCapture())
    with pytest.raises(RuntimeError):
        list(OpenCVCamera(0).frames())
