from __future__ import annotations

import cv2
import numpy as np

from sentinel_engine.anomaly import AnomalyDetector
from sentinel_engine.frameskip import FrameGate
from sentinel_engine.pipeline import Pipeline
from sentinel_engine.store import PerceptionStore
from sentinel_engine.teach import RecentFrames
from sentinel_engine.types import Image, Vector


class FakeEmbedder:
    dim = 192

    def embed(self, image_bgr: Image) -> Vector:
        small = cv2.resize(image_bgr, (8, 8), interpolation=cv2.INTER_AREA)
        return small.astype(np.float32).flatten()


def make_engine(
    *, warmup: int = 8, sensitivity: float = 0.5
) -> tuple[Pipeline, PerceptionStore, AnomalyDetector, RecentFrames]:
    store = PerceptionStore.in_memory("test", "clip", dim=FakeEmbedder.dim)
    detector = AnomalyDetector(warmup=warmup, window=50, sensitivity=sensitivity)
    recent = RecentFrames(256)
    pipeline = Pipeline(
        embedder=FakeEmbedder(),
        store=store,
        gate=FrameGate(0),
        detector=detector,
        top_k=3,
        recent=recent,
    )
    return pipeline, store, detector, recent
