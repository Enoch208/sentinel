from __future__ import annotations

import threading
import time
from collections import deque
from pathlib import Path

from pydantic import ValidationError

from sentinel_engine.anomaly import AnomalyDetector
from sentinel_engine.codec import to_jpeg_base64
from sentinel_engine.config import Settings
from sentinel_engine.embed import Embedder
from sentinel_engine.explore import Explorer
from sentinel_engine.frameskip import FrameGate
from sentinel_engine.metrics import footprint_mb
from sentinel_engine.pipeline import Pipeline
from sentinel_engine.protocol import (
    COMMAND_ADAPTER,
    AckEvent,
    ClusterModel,
    ExportCommand,
    FacetCommand,
    FacetEvent,
    FrameEvent,
    MetricEvent,
    ReportCommand,
    ReportEvent,
    ResetCommand,
    SensitivityCommand,
    TeachCommand,
    TwinsCommand,
    TwinsEvent,
    VerdictEvent,
    ZoneCommand,
    ZoneFacet,
)
from sentinel_engine.session import SessionLog
from sentinel_engine.store import PerceptionStore
from sentinel_engine.teach import RecentFrames, TeachController
from sentinel_engine.types import Frame
from sentinel_engine.watcher import AnomalyRecord, cluster_anomalies


class EngineController:
    def __init__(
        self,
        pipeline: Pipeline,
        store: PerceptionStore,
        detector: AnomalyDetector,
        teach: TeachController,
        explorer: Explorer,
        recent: RecentFrames,
        session: SessionLog | None = None,
        fps_window: int = 30,
        jpeg_width: int = 480,
        jpeg_quality: int = 70,
    ) -> None:
        self._pipeline = pipeline
        self._store = store
        self._detector = detector
        self._teach = teach
        self._explorer = explorer
        self._recent = recent
        self._session = session
        self._lock = threading.Lock()
        self._stamps: deque[float] = deque(maxlen=fps_window)
        self._jpeg_width = jpeg_width
        self._jpeg_quality = jpeg_quality
        self._zone = "default"
        self._zone_flags: dict[str, int] = {}
        self._anomalies: list[AnomalyRecord] = []

    def frame_event(self, frame: Frame) -> FrameEvent:
        jpeg = to_jpeg_base64(frame.image, self._jpeg_width, self._jpeg_quality)
        return FrameEvent(frame_id=frame.id, ts=frame.ts, jpeg=jpeg)

    def process_frame(self, frame: Frame) -> VerdictEvent | None:
        with self._lock:
            verdict = self._pipeline.process(frame)
            if verdict is None:
                return None
            self._stamps.append(time.monotonic())
            if verdict.flagged:
                self._zone_flags[self._zone] = self._zone_flags.get(self._zone, 0) + 1
                vector = self._recent.get(verdict.frame_id)
                if vector is not None:
                    self._anomalies.append(
                        AnomalyRecord(
                            frame_id=verdict.frame_id,
                            ts=verdict.ts,
                            zone=self._zone,
                            vector=vector,
                        )
                    )
            return VerdictEvent.of(verdict)

    def metrics(self) -> MetricEvent:
        with self._lock:
            pipeline = self._pipeline
            anomaly_ms = (
                pipeline.last_embed_ms
                + pipeline.last_query_ms
                + pipeline.last_decide_ms
            )
            return MetricEvent(
                fps=self._fps(),
                embed_ms=pipeline.last_embed_ms,
                query_ms=pipeline.last_query_ms,
                anomaly_ms=anomaly_ms,
                memory_mb=footprint_mb(),
                point_count=self._store.count(),
                quantized=self._store.quantization_active,
            )

    def handle_command(
        self, raw: object
    ) -> AckEvent | TwinsEvent | FacetEvent | ReportEvent:
        try:
            command = COMMAND_ADAPTER.validate_python(raw)
        except ValidationError as error:
            return AckEvent(command="unknown", ok=False, detail=str(error))
        with self._lock:
            return self._dispatch(command)

    def _fps(self) -> float:
        if len(self._stamps) < 2:
            return 0.0
        span = self._stamps[-1] - self._stamps[0]
        if span <= 0.0:
            return 0.0
        return (len(self._stamps) - 1) / span

    def _dispatch(
        self,
        command: SensitivityCommand
        | TeachCommand
        | TwinsCommand
        | ResetCommand
        | ExportCommand
        | ZoneCommand
        | FacetCommand
        | ReportCommand,
    ) -> AckEvent | TwinsEvent | FacetEvent | ReportEvent:
        if isinstance(command, SensitivityCommand):
            self._detector.set_sensitivity(command.value)
            return AckEvent(
                command="sensitivity",
                ok=True,
                detail=f"{self._detector.sensitivity:.2f}",
            )
        if isinstance(command, TeachCommand):
            result = (
                self._teach.expected(command.frame_id)
                if command.label == "expected"
                else self._teach.anomaly(command.frame_id)
            )
            return AckEvent(command="teach", ok=result.applied, detail=command.label)
        if isinstance(command, TwinsCommand):
            twins = self._explorer.twins(command.frame_id, command.k)
            return TwinsEvent.of(command.frame_id, twins)
        if isinstance(command, ZoneCommand):
            self._zone = command.zone
            self._pipeline.zone = command.zone
            return AckEvent(command="zone", ok=True, detail=command.zone)
        if isinstance(command, FacetCommand):
            return self._facets()
        if isinstance(command, ReportCommand):
            return self._report()
        if isinstance(command, ResetCommand):
            self._store.reset()
            self._detector.reset()
            self._recent.clear()
            self._zone_flags.clear()
            self._anomalies.clear()
            return AckEvent(command="reset", ok=True)
        if self._session is None:
            return AckEvent(command="export", ok=False, detail="no session")
        self._session.export(Path(command.path))
        return AckEvent(command="export", ok=True, detail=command.path)

    def _facets(self) -> FacetEvent:
        memory = self._store.facet("zone")
        zones = sorted(set(memory) | set(self._zone_flags))
        return FacetEvent(
            facets=[
                ZoneFacet(
                    zone=zone,
                    memory=memory.get(zone, 0),
                    flags=self._zone_flags.get(zone, 0),
                )
                for zone in zones
            ]
        )

    def _report(self) -> ReportEvent:
        report = cluster_anomalies(self._anomalies)
        return ReportEvent(
            total=report.total,
            clusters=[
                ClusterModel(
                    size=cluster.size,
                    exemplar_id=cluster.exemplar_id,
                    zones=list(cluster.zones),
                )
                for cluster in report.clusters
            ],
        )


def build_controller(
    settings: Settings,
    embedder: Embedder,
    *,
    in_memory: bool = False,
    session: SessionLog | None = None,
) -> EngineController:
    if in_memory:
        store = PerceptionStore.in_memory(
            settings.collection, settings.vector_name, embedder.dim
        )
    else:
        store = PerceptionStore.open(
            settings.db_path,
            settings.collection,
            settings.vector_name,
            embedder.dim,
            settings.quantize,
        )
    detector = AnomalyDetector(
        settings.warmup_frames, settings.window, settings.sensitivity, settings.margin
    )
    recent = RecentFrames(capacity=256)
    pipeline = Pipeline(
        embedder=embedder,
        store=store,
        gate=FrameGate(settings.skip_hamming),
        detector=detector,
        top_k=settings.top_k,
        session=session,
        recent=recent,
    )
    teach = TeachController(store, recent)
    explorer = Explorer(store, recent)
    return EngineController(
        pipeline,
        store,
        detector,
        teach,
        explorer,
        recent,
        session,
        jpeg_width=settings.jpeg_width,
        jpeg_quality=settings.jpeg_quality,
    )
