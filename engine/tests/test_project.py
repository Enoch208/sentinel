from __future__ import annotations

import numpy as np

from sentinel_engine.project import project_2d


def test_single_vector_returns_origin() -> None:
    coords = project_2d([np.array([1, 0, 0, 0], dtype=np.float32)])
    assert coords.shape == (1, 2)


def test_separates_two_clusters_on_an_axis() -> None:
    group_a = [np.array([1, 0, 0, 0], dtype=np.float32) for _ in range(4)]
    group_b = [np.array([0, 1, 0, 0], dtype=np.float32) for _ in range(4)]
    coords = project_2d([*group_a, *group_b])

    assert coords.shape == (8, 2)
    assert float(np.abs(coords).max()) <= 1.0 + 1e-6
    mean_a = coords[:4].mean(axis=0)
    mean_b = coords[4:].mean(axis=0)
    assert np.linalg.norm(mean_a - mean_b) > 0.5
