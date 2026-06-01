from __future__ import annotations

import numpy as np

from sentinel_engine.store import PerceptionStore


def _store() -> PerceptionStore:
    return PerceptionStore.in_memory("test", "clip", dim=4)


def test_upsert_and_count() -> None:
    store = _store()
    store.upsert(1, np.array([1, 0, 0, 0], dtype=np.float32), {"flagged": False})
    store.upsert(2, np.array([0, 1, 0, 0], dtype=np.float32), {"flagged": False})
    assert store.count() == 2


def test_query_returns_nearest() -> None:
    store = _store()
    store.upsert(1, np.array([1, 0, 0, 0], dtype=np.float32), {})
    store.upsert(2, np.array([0, 1, 0, 0], dtype=np.float32), {})
    store.upsert(3, np.array([0, 0, 1, 0], dtype=np.float32), {})

    neighbors = store.query(np.array([0, 0.9, 0, 0], dtype=np.float32), k=3)
    assert neighbors[0].id == 2
    assert neighbors[0].score > 0.9


def test_query_empty_collection() -> None:
    assert _store().query(np.array([1, 0, 0, 0], dtype=np.float32), k=3) == []
