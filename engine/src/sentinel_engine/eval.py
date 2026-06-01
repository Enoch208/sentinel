from __future__ import annotations

from dataclasses import dataclass

from sentinel_engine.anomaly import AnomalyDetector
from sentinel_engine.capture import SyntheticScene
from sentinel_engine.embed import Embedder
from sentinel_engine.frameskip import FrameGate
from sentinel_engine.pipeline import Pipeline
from sentinel_engine.store import PerceptionStore


@dataclass(frozen=True, slots=True)
class DetectionScore:
    precision: float
    recall: float
    f1: float
    flagged: int
    anomalies: int
    scored: int


def evaluate_detection(flags: list[bool], labels: list[bool]) -> DetectionScore:
    if len(flags) != len(labels):
        raise ValueError("flags and labels must align")
    pairs = list(zip(flags, labels, strict=True))
    tp = sum(1 for flag, label in pairs if flag and label)
    fp = sum(1 for flag, label in pairs if flag and not label)
    fn = sum(1 for flag, label in pairs if not flag and label)
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    denom = precision + recall
    f1 = 2 * precision * recall / denom if denom else 0.0
    return DetectionScore(
        precision=precision,
        recall=recall,
        f1=f1,
        flagged=sum(flags),
        anomalies=sum(labels),
        scored=len(flags),
    )


def run_synthetic_eval(
    embedder: Embedder,
    *,
    total: int = 60,
    anomaly_at: tuple[int, ...] = (40, 41, 42),
    warmup: int = 12,
    sensitivity: float = 0.5,
) -> DetectionScore:
    store = PerceptionStore.in_memory("eval", "clip", dim=embedder.dim)
    detector = AnomalyDetector(warmup=warmup, window=50, sensitivity=sensitivity)
    pipeline = Pipeline(
        embedder=embedder,
        store=store,
        gate=FrameGate(0),
        detector=detector,
        top_k=5,
    )
    anomalies = set(anomaly_at)

    flags: list[bool] = []
    labels: list[bool] = []
    for frame in SyntheticScene(total=total, anomaly_at=anomaly_at).frames():
        verdict = pipeline.process(frame)
        if verdict is None or verdict.warming:
            continue
        flags.append(verdict.flagged)
        labels.append(frame.id in anomalies)

    return evaluate_detection(flags, labels)


def main() -> int:
    from sentinel_engine.config import Settings
    from sentinel_engine.embed import FastEmbedImageEmbedder

    settings = Settings()
    print(f"loading model {settings.model_name}…")
    embedder = FastEmbedImageEmbedder(settings.model_name, settings.cache_dir)
    score = run_synthetic_eval(embedder)
    print("\nstaged-scene detection (synthetic):")
    print(f"  precision : {score.precision:.3f}")
    print(f"  recall    : {score.recall:.3f}")
    print(f"  f1        : {score.f1:.3f}")
    print(f"  flagged   : {score.flagged} / {score.scored} scored frames")
    print(f"  anomalies : {score.anomalies}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
