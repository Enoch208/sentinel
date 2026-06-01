from __future__ import annotations

import base64
from typing import cast

import cv2

from sentinel_engine.types import Image


def to_jpeg_base64(image: Image, max_width: int = 480, quality: int = 70) -> str:
    resized = _downscale(image, max_width)
    ok, buffer = cv2.imencode(".jpg", resized, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        raise ValueError("failed to encode frame as jpeg")
    return base64.b64encode(buffer.tobytes()).decode("ascii")


def _downscale(image: Image, max_width: int) -> Image:
    height, width = image.shape[:2]
    if width <= max_width:
        return image
    scale = max_width / width
    size = (max_width, int(height * scale))
    return cast(Image, cv2.resize(image, size, interpolation=cv2.INTER_AREA))
