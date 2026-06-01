from __future__ import annotations

from support import make_engine

from sentinel_engine.capture import SyntheticScene
from sentinel_engine.explore import Explorer


def test_twins_returns_similar_excluding_self() -> None:
    pipeline, store, _detector, recent = make_engine()
    for frame in SyntheticScene(total=15, anomaly_at=()).frames():
        pipeline.process(frame)

    explorer = Explorer(store, recent)
    twins = explorer.twins(frame_id=5, k=3)

    assert len(twins) == 3
    assert all(neighbor.id != 5 for neighbor in twins)


def test_twins_of_unknown_frame_is_empty() -> None:
    _pipeline, store, _detector, recent = make_engine()
    explorer = Explorer(store, recent)
    assert explorer.twins(frame_id=999, k=3) == []
