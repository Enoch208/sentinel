from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

Vector = NDArray[np.float32]
Image = NDArray[np.uint8]


@dataclass(frozen=True, slots=True)
class Frame:
    id: int
    ts: float
    image: Image


@dataclass(frozen=True, slots=True)
class Neighbor:
    id: int
    score: float


@dataclass(frozen=True, slots=True)
class Verdict:
    frame_id: int
    ts: float
    score: float | None
    threshold: float
    flagged: bool
    warming: bool
    neighbors: list[Neighbor]


@dataclass(frozen=True, slots=True)
class Metric:
    fps: float
    embed_ms: float
    query_ms: float
    point_count: int
