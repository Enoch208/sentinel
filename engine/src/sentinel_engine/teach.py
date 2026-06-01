from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass

from sentinel_engine.store import PerceptionStore
from sentinel_engine.types import Vector


class RecentFrames:
    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._items: OrderedDict[int, Vector] = OrderedDict()

    def add(self, frame_id: int, vector: Vector) -> None:
        self._items[frame_id] = vector
        self._items.move_to_end(frame_id)
        while len(self._items) > self._capacity:
            self._items.popitem(last=False)

    def get(self, frame_id: int) -> Vector | None:
        return self._items.get(frame_id)

    def clear(self) -> None:
        self._items.clear()


@dataclass(frozen=True, slots=True)
class TeachResult:
    frame_id: int
    label: str
    applied: bool


class TeachController:
    def __init__(self, store: PerceptionStore, recent: RecentFrames) -> None:
        self._store = store
        self._recent = recent
        self._negatives: list[int] = []

    @property
    def negatives(self) -> list[int]:
        return list(self._negatives)

    def expected(self, frame_id: int) -> TeachResult:
        vector = self._recent.get(frame_id)
        if vector is None:
            return TeachResult(frame_id, "expected", False)
        self._store.upsert(
            frame_id, vector, {"ts": 0.0, "flagged": False, "label": "expected"}
        )
        if frame_id in self._negatives:
            self._negatives.remove(frame_id)
        return TeachResult(frame_id, "expected", True)

    def anomaly(self, frame_id: int) -> TeachResult:
        vector = self._recent.get(frame_id)
        self._store.delete(frame_id)
        if frame_id not in self._negatives:
            self._negatives.append(frame_id)
        return TeachResult(frame_id, "anomaly", vector is not None)
