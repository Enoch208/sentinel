from __future__ import annotations

import threading
import time
from collections.abc import Iterator
from typing import Protocol, cast

import numpy as np

from sentinel_engine.types import Frame, Image


class FrameSource(Protocol):
    def frames(self) -> Iterator[Frame]: ...


class OpenCVCamera:
    def __init__(self, index: int = 0) -> None:
        self._index = index

    def frames(self) -> Iterator[Frame]:
        import cv2

        capture = cv2.VideoCapture(self._index)
        if not capture.isOpened():
            raise RuntimeError(f"could not open camera {self._index}")
        index = 0
        try:
            while True:
                ok, image = capture.read()
                if not ok:
                    break
                frame_image = cast(Image, np.asarray(image, dtype=np.uint8))
                yield Frame(id=index, ts=time.time(), image=frame_image)
                index += 1
        finally:
            capture.release()


class LatestFrameCamera:
    def __init__(self, index: int = 0, width: int = 640, height: int = 480) -> None:
        self._index = index
        self._width = width
        self._height = height

    def frames(self) -> Iterator[Frame]:
        import cv2

        capture = cv2.VideoCapture(self._index)
        if not capture.isOpened():
            raise RuntimeError(f"could not open camera {self._index}")
        capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)

        stop = threading.Event()
        lock = threading.Lock()
        state: dict[str, object] = {"image": None, "id": -1, "done": False}

        def grab() -> None:
            index = 0
            while not stop.is_set():
                ok, image = capture.read()
                if not ok:
                    break
                with lock:
                    state["image"] = image
                    state["id"] = index
                index += 1
            with lock:
                state["done"] = True

        worker = threading.Thread(target=grab, daemon=True)
        worker.start()

        last = -1
        try:
            while not stop.is_set():
                with lock:
                    image = state["image"]
                    current = cast(int, state["id"])
                    done = cast(bool, state["done"])
                if image is not None and current != last:
                    last = current
                    pixels = cast(Image, np.asarray(image, dtype=np.uint8))
                    yield Frame(id=current, ts=time.time(), image=pixels)
                    continue
                if done:
                    break
                time.sleep(0.005)
        finally:
            stop.set()
            worker.join(timeout=1.0)
            capture.release()


class SyntheticScene:
    def __init__(
        self,
        total: int = 40,
        anomaly_at: tuple[int, ...] = (24, 25, 26),
        height: int = 180,
        width: int = 320,
        seed: int = 7,
    ) -> None:
        self._total = total
        self._anomaly_at = set(anomaly_at)
        self._height = height
        self._width = width
        self._rng = np.random.default_rng(seed)
        self._base = self._make_base()

    def _make_base(self) -> Image:
        ramp = np.linspace(20, 200, self._width, dtype=np.float32)
        plane = np.tile(ramp, (self._height, 1))
        image = np.stack([plane, plane * 0.6, plane * 0.3], axis=2)
        return cast(Image, image.astype(np.uint8))

    def _normal(self) -> Image:
        noise = self._rng.normal(0.0, 4.0, self._base.shape).astype(np.float32)
        blended = np.clip(self._base.astype(np.float32) + noise, 0, 255)
        return cast(Image, blended.astype(np.uint8))

    def _anomaly(self) -> Image:
        image = self._normal()
        h0 = self._height // 4
        w0 = self._width // 4
        image[h0 : h0 * 3, w0 : w0 * 3] = (255, 0, 255)
        return image

    def frames(self) -> Iterator[Frame]:
        for index in range(self._total):
            image = self._anomaly() if index in self._anomaly_at else self._normal()
            yield Frame(id=index, ts=float(index), image=image)
