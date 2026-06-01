from __future__ import annotations

from support import FakeEmbedder

from sentinel_engine.anomaly import AnomalyDetector
from sentinel_engine.capture import SyntheticScene
from sentinel_engine.frameskip import FrameGate
from sentinel_engine.pipeline import Pipeline
from sentinel_engine.store import PerceptionStore


def _pipeline() -> tuple[Pipeline, PerceptionStore]:
    store = PerceptionStore.in_memory("flow", "clip", dim=FakeEmbedder.dim)
    detector = AnomalyDetector(warmup=8, window=50, sensitivity=0.5)
    pipeline = Pipeline(
        embedder=FakeEmbedder(),
        store=store,
        gate=FrameGate(hamming_threshold=0),
        detector=detector,
        top_k=3,
    )
    return pipeline, store


def test_flags_the_out_of_place_object_and_recovers() -> None:
    pipeline, store = _pipeline()
    scene = SyntheticScene(total=40, anomaly_at=(24, 25, 26))

    verdicts = {}
    for frame in scene.frames():
        verdict = pipeline.process(frame)
        assert verdict is not None
        verdicts[frame.id] = verdict

    assert verdicts[2].warming is True
    assert verdicts[20].warming is False
    assert verdicts[20].flagged is False

    assert verdicts[24].flagged is True
    assert verdicts[25].flagged is True

    assert verdicts[30].flagged is False


def test_a_persistent_new_scene_keeps_flagging() -> None:
    pipeline, _store = _pipeline()
    frames = list(SyntheticScene(total=40, anomaly_at=tuple(range(20, 40))).frames())

    flagged_tail = []
    for frame in frames:
        verdict = pipeline.process(frame)
        assert verdict is not None
        if frame.id >= 22 and not verdict.warming:
            flagged_tail.append(verdict.flagged)

    assert len(flagged_tail) > 5
    assert all(flagged_tail)


def test_anomaly_frames_are_not_learned_as_normal() -> None:
    pipeline, store = _pipeline()
    scene = SyntheticScene(total=40, anomaly_at=(24, 25, 26))

    count_before = None
    for frame in scene.frames():
        if frame.id == 24:
            count_before = store.count()
        pipeline.process(frame)
        if frame.id == 26:
            assert store.count() == count_before
            return

    raise AssertionError("anomaly frames were not reached")
