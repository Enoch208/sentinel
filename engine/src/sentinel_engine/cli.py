from __future__ import annotations

import argparse
from pathlib import Path

from sentinel_engine.anomaly import AnomalyDetector
from sentinel_engine.capture import FrameSource, OpenCVCamera, SyntheticScene
from sentinel_engine.config import Settings
from sentinel_engine.embed import FastEmbedImageEmbedder
from sentinel_engine.frameskip import FrameGate
from sentinel_engine.pipeline import Pipeline
from sentinel_engine.session import SessionLog
from sentinel_engine.store import PerceptionStore
from sentinel_engine.types import Verdict


def _render(verdict: Verdict) -> str:
    if verdict.warming:
        return f"frame {verdict.frame_id:>4}  learning normal…"
    score = "  n/a" if verdict.score is None else f"{verdict.score:.3f}"
    if verdict.flagged:
        return (
            f"frame {verdict.frame_id:>4}  ⚠ OUT OF PLACE  "
            f"score={score} < threshold={verdict.threshold:.3f}"
        )
    return (
        f"frame {verdict.frame_id:>4}  normal           "
        f"score={score}  threshold={verdict.threshold:.3f}"
    )


def main() -> int:
    defaults = Settings()
    parser = argparse.ArgumentParser(prog="sentinel")
    parser.add_argument("--synthetic", action="store_true")
    parser.add_argument("--db", default=None)
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--frames", type=int, default=40)
    parser.add_argument("--sensitivity", type=float, default=defaults.sensitivity)
    args = parser.parse_args()

    settings = Settings(sensitivity=args.sensitivity)
    if args.db:
        settings.db_path = args.db

    print(f"loading model {settings.model_name} (first run downloads it)…")
    embedder = FastEmbedImageEmbedder(settings.model_name)
    store = PerceptionStore.open(
        settings.db_path,
        settings.collection,
        settings.vector_name,
        embedder.dim,
        settings.quantize,
    )
    detector = AnomalyDetector(
        settings.warmup_frames,
        settings.window,
        settings.sensitivity,
        settings.margin,
    )
    session = SessionLog(Path("sessions") / "session.jsonl")
    pipeline = Pipeline(
        embedder=embedder,
        store=store,
        gate=FrameGate(settings.skip_hamming),
        detector=detector,
        top_k=settings.top_k,
        session=session,
    )

    source: FrameSource = (
        SyntheticScene(total=args.frames)
        if args.synthetic
        else OpenCVCamera(args.camera)
    )

    print("watching — Ctrl-C to stop. (offline; nothing leaves this machine)\n")
    flags = 0
    try:
        for frame in source.frames():
            verdict = pipeline.process(frame)
            if verdict is None:
                continue
            flags += int(verdict.flagged)
            print(_render(verdict))
    except KeyboardInterrupt:
        pass

    print(f"\nkept memory: {store.count()} points · flags raised: {flags}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
