from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter

from sentinel_engine.types import Neighbor, Verdict


class NeighborModel(BaseModel):
    id: int
    score: float

    @classmethod
    def of_many(cls, neighbors: list[Neighbor]) -> list[NeighborModel]:
        return [cls(id=n.id, score=n.score) for n in neighbors]


class VerdictEvent(BaseModel):
    type: Literal["verdict"] = "verdict"
    frame_id: int
    ts: float
    score: float | None
    threshold: float
    flagged: bool
    warming: bool
    neighbors: list[NeighborModel]

    @classmethod
    def of(cls, verdict: Verdict) -> VerdictEvent:
        return cls(
            frame_id=verdict.frame_id,
            ts=verdict.ts,
            score=verdict.score,
            threshold=verdict.threshold,
            flagged=verdict.flagged,
            warming=verdict.warming,
            neighbors=NeighborModel.of_many(verdict.neighbors),
        )


class FrameEvent(BaseModel):
    type: Literal["frame"] = "frame"
    frame_id: int
    ts: float
    jpeg: str


class MetricEvent(BaseModel):
    type: Literal["metric"] = "metric"
    fps: float
    embed_ms: float
    query_ms: float
    anomaly_ms: float
    memory_mb: float
    point_count: int
    quantized: bool


class TwinsEvent(BaseModel):
    type: Literal["twins"] = "twins"
    frame_id: int
    results: list[NeighborModel]

    @classmethod
    def of(cls, frame_id: int, neighbors: list[Neighbor]) -> TwinsEvent:
        return cls(frame_id=frame_id, results=NeighborModel.of_many(neighbors))


class ZoneFacet(BaseModel):
    zone: str
    memory: int
    flags: int


class FacetEvent(BaseModel):
    type: Literal["facet"] = "facet"
    facets: list[ZoneFacet]


class ClusterModel(BaseModel):
    size: int
    exemplar_id: int
    zones: list[str]


class ReportEvent(BaseModel):
    type: Literal["report"] = "report"
    total: int
    clusters: list[ClusterModel]


class MapPoint(BaseModel):
    id: int
    x: float
    y: float
    flagged: bool
    zone: str


class MapEvent(BaseModel):
    type: Literal["map"] = "map"
    points: list[MapPoint]


class AckEvent(BaseModel):
    type: Literal["ack"] = "ack"
    command: str
    ok: bool
    detail: str = ""


class SensitivityCommand(BaseModel):
    type: Literal["sensitivity"]
    value: float


class TeachCommand(BaseModel):
    type: Literal["teach"]
    frame_id: int
    label: Literal["expected", "anomaly"]


class TwinsCommand(BaseModel):
    type: Literal["twins"]
    frame_id: int
    k: int = 3


class ResetCommand(BaseModel):
    type: Literal["reset"]


class ExportCommand(BaseModel):
    type: Literal["export"]
    path: str


class ZoneCommand(BaseModel):
    type: Literal["zone"]
    zone: str


class FacetCommand(BaseModel):
    type: Literal["facet"]


class ReportCommand(BaseModel):
    type: Literal["report"]


class MapCommand(BaseModel):
    type: Literal["map"]


Command = Annotated[
    SensitivityCommand
    | TeachCommand
    | TwinsCommand
    | ResetCommand
    | ExportCommand
    | ZoneCommand
    | FacetCommand
    | ReportCommand
    | MapCommand,
    Field(discriminator="type"),
]

COMMAND_ADAPTER: TypeAdapter[Command] = TypeAdapter(Command)
