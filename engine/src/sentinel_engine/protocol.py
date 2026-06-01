from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter

from sentinel_engine.types import Neighbor, Verdict


class NeighborModel(BaseModel):
    id: int
    score: float


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
            neighbors=[
                NeighborModel(id=n.id, score=n.score) for n in verdict.neighbors
            ],
        )


class MetricEvent(BaseModel):
    type: Literal["metric"] = "metric"
    fps: float
    embed_ms: float
    query_ms: float
    point_count: int


class TwinsEvent(BaseModel):
    type: Literal["twins"] = "twins"
    frame_id: int
    results: list[NeighborModel]

    @classmethod
    def of(cls, frame_id: int, neighbors: list[Neighbor]) -> TwinsEvent:
        return cls(
            frame_id=frame_id,
            results=[NeighborModel(id=n.id, score=n.score) for n in neighbors],
        )


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


Command = Annotated[
    SensitivityCommand | TeachCommand | TwinsCommand | ResetCommand | ExportCommand,
    Field(discriminator="type"),
]

COMMAND_ADAPTER: TypeAdapter[Command] = TypeAdapter(Command)
