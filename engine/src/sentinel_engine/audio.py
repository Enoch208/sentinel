from __future__ import annotations

from collections.abc import Iterator
from typing import cast

import numpy as np

from sentinel_engine.anomaly import AnomalyDetector
from sentinel_engine.store import PerceptionStore
from sentinel_engine.types import Neighbor, Vector, Verdict


class AudioEmbedder:
    def __init__(self, sample_rate: int = 16000, bands: int = 32) -> None:
        self._sample_rate = sample_rate
        self._bands = bands

    @property
    def dim(self) -> int:
        return self._bands

    def embed(self, chunk: Vector) -> Vector:
        window = np.hanning(len(chunk)).astype(np.float32)
        spectrum = np.abs(np.fft.rfft(chunk * window))
        freqs = np.fft.rfftfreq(len(chunk), 1.0 / self._sample_rate)
        edges = np.logspace(
            np.log10(20.0), np.log10(self._sample_rate / 2.0), self._bands + 1
        )
        feature = np.zeros(self._bands, dtype=np.float32)
        for index in range(self._bands):
            band = (freqs >= edges[index]) & (freqs < edges[index + 1])
            if band.any():
                feature[index] = float(spectrum[band].mean())
        return cast(Vector, np.log1p(feature).astype(np.float32))


class SyntheticAudioScene:
    def __init__(
        self,
        total: int = 40,
        anomaly_at: tuple[int, ...] = (24, 25, 26),
        sample_rate: int = 16000,
        duration: float = 0.25,
        seed: int = 11,
    ) -> None:
        self._total = total
        self._anomaly_at = set(anomaly_at)
        self._sample_rate = sample_rate
        self._samples = int(sample_rate * duration)
        self._rng = np.random.default_rng(seed)

    def _tone(self, freq: float) -> Vector:
        t = np.arange(self._samples) / self._sample_rate
        noise = self._rng.normal(0.0, 0.02, self._samples)
        signal = np.sin(2.0 * np.pi * freq * t) + noise
        return cast(Vector, signal.astype(np.float32))

    def chunks(self) -> Iterator[tuple[int, Vector]]:
        for index in range(self._total):
            freq = 2000.0 if index in self._anomaly_at else 440.0
            yield index, self._tone(freq)


class AudioMonitor:
    def __init__(
        self,
        embedder: AudioEmbedder,
        store: PerceptionStore,
        detector: AnomalyDetector,
        top_k: int = 5,
    ) -> None:
        self._embedder = embedder
        self._store = store
        self._detector = detector
        self._k = top_k

    def process(self, index: int, chunk: Vector) -> Verdict:
        vector = self._embedder.embed(chunk)
        neighbors: list[Neighbor] = self._store.query(vector, self._k)
        top = neighbors[0].score if neighbors else None
        decision = self._detector.decide(top, self._store.count())
        if not decision.flagged:
            self._store.upsert(index, vector, {"flagged": False})
            if top is not None:
                self._detector.observe(top)
        return Verdict(
            frame_id=index,
            ts=float(index),
            score=top,
            threshold=decision.threshold,
            flagged=decision.flagged,
            warming=decision.warming,
            neighbors=neighbors,
        )


def _render(verdict: Verdict) -> str:
    if verdict.warming:
        return f"chunk {verdict.frame_id:>4}  learning normal sound…"
    score = "  n/a" if verdict.score is None else f"{verdict.score:.3f}"
    if verdict.flagged:
        return f"chunk {verdict.frame_id:>4}  ⚠ OUT-OF-PLACE SOUND  score={score}"
    return f"chunk {verdict.frame_id:>4}  normal sound          score={score}"


def main() -> int:
    embedder = AudioEmbedder()
    store = PerceptionStore.in_memory("sounds", "audio", dim=embedder.dim)
    detector = AnomalyDetector(warmup=12, window=50, sensitivity=0.5)
    monitor = AudioMonitor(embedder, store, detector)

    print("listening (synthetic) — offline; an out-of-place sound is flagged\n")
    flags = 0
    for index, chunk in SyntheticAudioScene().chunks():
        verdict = monitor.process(index, chunk)
        flags += int(verdict.flagged)
        print(_render(verdict))
    print(f"\nflags raised: {flags}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
