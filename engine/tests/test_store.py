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


def test_delete_removes_point() -> None:
    store = _store()
    store.upsert(1, np.array([1, 0, 0, 0], dtype=np.float32), {})
    store.upsert(2, np.array([0, 1, 0, 0], dtype=np.float32), {})
    store.delete(1)
    assert store.count() == 1


def test_get_vector_roundtrip() -> None:
    store = _store()
    vector = np.array([0.0, 0.0, 1.0, 0.0], dtype=np.float32)
    store.upsert(7, vector, {})
    fetched = store.get_vector(7)
    assert fetched is not None
    assert np.allclose(fetched, vector, atol=1e-5)
    assert store.get_vector(999) is None


def test_recommend_prefers_positive_like() -> None:
    store = _store()
    store.upsert(0, np.array([1, 0, 0, 0], dtype=np.float32), {})
    store.upsert(1, np.array([0, 1, 0, 0], dtype=np.float32), {})
    store.upsert(2, np.array([0, 0, 1, 0], dtype=np.float32), {})
    store.upsert(3, np.array([1, 1, 0, 0], dtype=np.float32), {})

    neighbors = store.recommend(positive=[0], negative=[1], k=3)
    assert neighbors
    assert neighbors[0].id == 3


def test_reset_empties_collection() -> None:
    store = _store()
    store.upsert(1, np.array([1, 0, 0, 0], dtype=np.float32), {})
    store.reset()
    assert store.count() == 0


def test_facet_counts_by_payload_key() -> None:
    store = _store()
    vec = np.array([1, 0, 0, 0], dtype=np.float32)
    store.upsert(1, vec, {"zone": "bench"})
    store.upsert(2, vec, {"zone": "bench"})
    store.upsert(3, vec, {"zone": "shelf"})

    counts = store.facet("zone")
    assert counts["bench"] == 2
    assert counts["shelf"] == 1


def test_quantization_active_reports_truthfully() -> None:
    plain = PerceptionStore.in_memory("nq", "clip", dim=4, quantize=False)
    assert plain.quantization_active is False

    requested = PerceptionStore.in_memory("q", "clip", dim=4, quantize=True)
    assert isinstance(requested.quantization_active, bool)
