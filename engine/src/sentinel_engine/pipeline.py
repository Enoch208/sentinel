from __future__ import annotations

from sentinel_engine.anomaly import AnomalyDetector
from sentinel_engine.embed import Embedder
from sentinel_engine.frameskip import FrameGate
from sentinel_engine.session import SessionLog
from sentinel_engine.store import PerceptionStore
from sentinel_engine.types import Frame, Verdict


class Pipeline:
    def __init__(
        self,
        embedder: Embedder,
        store: PerceptionStore,
        gate: FrameGate,
        detector: AnomalyDetector,
        top_k: int,
        session: SessionLog | None = None,
    ) -> None:
        self._embedder = embedder
        self._store = store
        self._gate = gate
        self._detector = detector
        self._k = top_k
        self._session = session

    def process(self, frame: Frame) -> Verdict | None:
        if not self._gate.should_keep(frame.image):
            return None

        vector = self._embedder.embed(frame.image)
        neighbors = self._store.query(vector, self._k)
        top = neighbors[0].score if neighbors else None
        decision = self._detector.decide(top, self._store.count())

        if not decision.flagged:
            self._store.upsert(frame.id, vector, {"ts": frame.ts, "flagged": False})
            if top is not None:
                self._detector.observe(top)

        verdict = Verdict(
            frame_id=frame.id,
            ts=frame.ts,
            score=top,
            threshold=decision.threshold,
            flagged=decision.flagged,
            warming=decision.warming,
            neighbors=neighbors,
        )
        if self._session is not None:
            self._session.record(verdict)
        return verdict
