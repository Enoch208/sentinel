from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np
from PIL import Image as PILImage

from sentinel_engine.types import Image, Vector


@runtime_checkable
class Embedder(Protocol):
    @property
    def dim(self) -> int: ...

    def embed(self, image_bgr: Image) -> Vector: ...


class FastEmbedImageEmbedder:
    def __init__(self, model_name: str, cache_dir: str | None = None) -> None:
        from fastembed import ImageEmbedding

        catalog = {m["model"]: m for m in ImageEmbedding.list_supported_models()}
        if model_name not in catalog:
            raise ValueError(f"unknown image model: {model_name}")
        self._dim = int(catalog[model_name]["dim"])
        self._model = ImageEmbedding(model_name=model_name, cache_dir=cache_dir)

    @property
    def dim(self) -> int:
        return self._dim

    def embed(self, image_bgr: Image) -> Vector:
        rgb = np.ascontiguousarray(image_bgr[:, :, ::-1])
        pil = PILImage.fromarray(rgb)
        vector = next(iter(self._model.embed([pil])))
        return np.asarray(vector, dtype=np.float32)
