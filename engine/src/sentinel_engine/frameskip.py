from __future__ import annotations

import imagehash
import numpy as np
from PIL import Image as PILImage

from sentinel_engine.types import Image


class FrameGate:
    def __init__(self, hamming_threshold: int) -> None:
        self._threshold = hamming_threshold
        self._last: imagehash.ImageHash | None = None
        self._seen = 0
        self._kept = 0

    @property
    def seen(self) -> int:
        return self._seen

    @property
    def kept(self) -> int:
        return self._kept

    def should_keep(self, image_bgr: Image) -> bool:
        self._seen += 1
        rgb = np.ascontiguousarray(image_bgr[:, :, ::-1])
        digest = imagehash.phash(PILImage.fromarray(rgb))
        if self._last is None or (digest - self._last) >= self._threshold:
            self._last = digest
            self._kept += 1
            return True
        return False
