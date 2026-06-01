from __future__ import annotations

from sentinel_engine.store import PerceptionStore
from sentinel_engine.teach import RecentFrames
from sentinel_engine.types import Neighbor


class Explorer:
    def __init__(self, store: PerceptionStore, recent: RecentFrames) -> None:
        self._store = store
        self._recent = recent

    def twins(self, frame_id: int, k: int) -> list[Neighbor]:
        vector = self._recent.get(frame_id)
        if vector is None:
            vector = self._store.get_vector(frame_id)
        if vector is None:
            return []
        neighbors = self._store.query(vector, k + 1)
        return [n for n in neighbors if n.id != frame_id][:k]
