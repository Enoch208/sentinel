from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    collection: str = "perceptions"
    vector_name: str = "clip"
    model_name: str = "Qdrant/clip-ViT-B-32-vision"
    cache_dir: str = ".fastembed_cache"
    db_path: str = "./sentinel.db"
    qdrant_url: str | None = None
    top_k: int = 5
    skip_hamming: int = 8
    warmup_frames: int = 12
    window: int = 50
    sensitivity: float = 0.5
    margin: float = 0.05
    quantize: bool = True
    jpeg_width: int = 480
    jpeg_quality: int = 70


def apply_env_overrides(settings: Settings) -> Settings:
    db = os.environ.get("SENTINEL_DB")
    if db:
        settings.db_path = db
    cache = os.environ.get("SENTINEL_CACHE")
    if cache:
        settings.cache_dir = cache
    url = os.environ.get("SENTINEL_QDRANT_URL")
    if url:
        settings.qdrant_url = url
    quantize = os.environ.get("SENTINEL_QUANTIZE")
    if quantize is not None:
        settings.quantize = quantize.lower() not in ("0", "false", "no", "")
    return settings
