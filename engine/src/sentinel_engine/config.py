from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    collection: str = "perceptions"
    vector_name: str = "clip"
    model_name: str = "Qdrant/clip-ViT-B-32-vision"
    db_path: str = "./sentinel.db"
    top_k: int = 5
    skip_hamming: int = 8
    warmup_frames: int = 12
    window: int = 50
    sensitivity: float = 0.5
    margin: float = 0.05
    quantize: bool = True
    jpeg_width: int = 480
    jpeg_quality: int = 70
