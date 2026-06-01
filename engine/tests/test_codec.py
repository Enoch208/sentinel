from __future__ import annotations

import base64

import cv2
import numpy as np

from sentinel_engine.codec import to_jpeg_base64


def test_encodes_to_decodable_jpeg() -> None:
    image = np.zeros((180, 320, 3), dtype=np.uint8)
    image[40:120, 60:200] = (255, 0, 255)

    encoded = to_jpeg_base64(image, max_width=480, quality=70)
    assert isinstance(encoded, str)
    assert len(encoded) > 0

    raw = np.frombuffer(base64.b64decode(encoded), dtype=np.uint8)
    decoded = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    assert decoded is not None
    assert decoded.shape[2] == 3


def test_downscales_wide_frames() -> None:
    image = np.zeros((600, 1200, 3), dtype=np.uint8)
    encoded = to_jpeg_base64(image, max_width=480, quality=70)

    raw = np.frombuffer(base64.b64decode(encoded), dtype=np.uint8)
    decoded = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    assert decoded is not None
    assert decoded.shape[1] == 480


def test_keeps_small_frames_unscaled() -> None:
    image = np.zeros((90, 160, 3), dtype=np.uint8)
    encoded = to_jpeg_base64(image, max_width=480, quality=70)

    raw = np.frombuffer(base64.b64decode(encoded), dtype=np.uint8)
    decoded = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    assert decoded is not None
    assert decoded.shape[1] == 160
