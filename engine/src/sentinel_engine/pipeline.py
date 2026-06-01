from __future__ import annotations

import time

from sentinel_engine.anomaly import AnomalyDetector
from sentinel_engine.embed import Embedder
from sentinel_engine.frameskip import FrameGate
from sentinel_engine.session import SessionLog
from sentinel_engine.store import PerceptionStore
from sentinel_engine.teach import RecentFrames
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
        recent: RecentFrames | None = None,
    ) -> None:
        self._embedder = embedder
        self._store = store
        self._gate = gate
        self._detector = detector
        self._k = top_k
        self._session = session
        self._recent = recent
        self.zone = "default"
        self.last_embed_ms = 0.0
        self.last_query_ms = 0.0
        self.last_decide_ms = 0.0

    def process(self, frame: Frame) -> Verdict | None:
        if not self._gate.should_keep(frame.image):
            return None

        started = time.perf_counter()
        vector = self._embedder.embed(frame.image)
        embedded = time.perf_counter()
        neighbors = self._store.query(vector, self._k)
        queried = time.perf_counter()
        self.last_embed_ms = (embedded - started) * 1000.0
        self.last_query_ms = (queried - embedded) * 1000.0

        if self._recent is not None:
            self._recent.add(frame.id, vector)

        top = neighbors[0].score if neighbors else None
        decision = self._detector.decide(top, self._store.count())
        self.last_decide_ms = (time.perf_counter() - queried) * 1000.0

        if not decision.flagged:
            self._store.upsert(
                frame.id,
                vector,
                {"ts": frame.ts, "flagged": False, "zone": self.zone},
            )
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
