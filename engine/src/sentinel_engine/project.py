from __future__ import annotations

from collections.abc import Sequence
from typing import cast

import numpy as np
from numpy.typing import NDArray

from sentinel_engine.types import Vector


def project_2d(vectors: Sequence[Vector]) -> NDArray[np.float32]:
    if len(vectors) < 2:
        return np.zeros((len(vectors), 2), dtype=np.float32)

    matrix = np.stack(vectors).astype(np.float64)
    centered = matrix - matrix.mean(axis=0)
    _, _, components = np.linalg.svd(centered, full_matrices=False)
    coords = centered @ components[:2].T

    if coords.shape[1] < 2:
        coords = np.pad(coords, ((0, 0), (0, 2 - coords.shape[1])))

    span = float(np.abs(coords).max())
    if span > 0.0:
        coords = coords / span

    return cast(NDArray[np.float32], coords.astype(np.float32))
