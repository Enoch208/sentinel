from __future__ import annotations

import numpy as np

from sentinel_engine.anomaly import AnomalyDetector
from sentinel_engine.audio import AudioEmbedder, AudioMonitor, SyntheticAudioScene
from sentinel_engine.eval import evaluate_detection
from sentinel_engine.store import PerceptionStore
from sentinel_engine.types import Vector


def _tone(freq: float, samples: int = 4000, sample_rate: int = 16000) -> Vector:
    t = np.arange(samples) / sample_rate
    return np.sin(2.0 * np.pi * freq * t).astype(np.float32)


def _cosine(a: Vector, b: Vector) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def test_similar_sounds_embed_closer_than_different_ones() -> None:
    embedder = AudioEmbedder()
    same = _cosine(embedder.embed(_tone(440)), embedder.embed(_tone(450)))
    apart = _cosine(embedder.embed(_tone(440)), embedder.embed(_tone(3000)))
    assert same > apart


def _monitor() -> tuple[AudioMonitor, PerceptionStore]:
    embedder = AudioEmbedder()
    store = PerceptionStore.in_memory("sounds", "audio", dim=embedder.dim)
    detector = AnomalyDetector(warmup=8, window=50, sensitivity=0.5)
    return AudioMonitor(embedder, store, detector, top_k=3), store


def test_flags_the_out_of_place_sound_and_recovers() -> None:
    monitor, _store = _monitor()
    verdicts = {}
    for index, chunk in SyntheticAudioScene(total=40, anomaly_at=(24, 25, 26)).chunks():
        verdicts[index] = monitor.process(index, chunk)

    assert verdicts[2].warming is True
    assert verdicts[20].flagged is False
    assert verdicts[24].flagged is True
    assert verdicts[30].flagged is False


def test_synthetic_audio_detection_recall() -> None:
    monitor, _store = _monitor()
    anomalies = {24, 25, 26}
    flags: list[bool] = []
    labels: list[bool] = []
    for index, chunk in SyntheticAudioScene(total=40, anomaly_at=(24, 25, 26)).chunks():
        verdict = monitor.process(index, chunk)
        if verdict.warming:
            continue
        flags.append(verdict.flagged)
        labels.append(index in anomalies)

    score = evaluate_detection(flags, labels)
    assert score.recall == 1.0
