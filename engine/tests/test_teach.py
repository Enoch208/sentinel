from __future__ import annotations

import numpy as np
from support import make_engine

from sentinel_engine.capture import SyntheticScene
from sentinel_engine.teach import RecentFrames, TeachController


def test_recent_frames_evicts_oldest() -> None:
    recent = RecentFrames(2)
    vector = np.zeros(4, dtype=np.float32)
    recent.add(1, vector)
    recent.add(2, vector)
    recent.add(3, vector)
    assert recent.get(1) is None
    assert recent.get(3) is not None


def test_teaching_expected_stops_the_flag_next_time() -> None:
    pipeline, store, _detector, recent = make_engine()
    frames = list(SyntheticScene(total=22, anomaly_at=(20, 21)).frames())

    flagged_at_20 = False
    for frame in frames[:21]:
        verdict = pipeline.process(frame)
        if frame.id == 20 and verdict is not None:
            flagged_at_20 = verdict.flagged
    assert flagged_at_20 is True

    teach = TeachController(store, recent)
    assert teach.expected(20).applied is True

    after = pipeline.process(frames[21])
    assert after is not None
    assert after.flagged is False


def test_teaching_anomaly_removes_from_normal_memory() -> None:
    pipeline, store, _detector, recent = make_engine()
    for frame in SyntheticScene(total=20, anomaly_at=()).frames():
        pipeline.process(frame)

    before = store.count()
    teach = TeachController(store, recent)
    result = teach.anomaly(5)

    assert result.applied is True
    assert store.count() == before - 1
    assert 5 in teach.negatives
