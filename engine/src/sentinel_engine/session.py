from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from sentinel_engine.types import Verdict


class SessionLog:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._events: list[dict[str, Any]] = []

    @property
    def events(self) -> list[dict[str, Any]]:
        return list(self._events)

    def record(self, verdict: Verdict) -> None:
        event: dict[str, Any] = {
            "frame_id": verdict.frame_id,
            "ts": verdict.ts,
            "score": verdict.score,
            "threshold": verdict.threshold,
            "flagged": verdict.flagged,
            "warming": verdict.warming,
            "neighbors": [{"id": n.id, "score": n.score} for n in verdict.neighbors],
        }
        self._events.append(event)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event) + "\n")

    def export(self, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self._path, dest)

    @staticmethod
    def load(path: Path) -> list[dict[str, Any]]:
        with path.open(encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]
