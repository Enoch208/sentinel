from __future__ import annotations

from pathlib import Path

from sentinel_engine.session import SessionLog
from sentinel_engine.types import Neighbor, Verdict


def _verdict() -> Verdict:
    return Verdict(
        frame_id=24,
        ts=24.0,
        score=0.42,
        threshold=0.80,
        flagged=True,
        warming=False,
        neighbors=[Neighbor(id=3, score=0.42)],
    )


def test_records_and_persists(tmp_path: Path) -> None:
    log = SessionLog(tmp_path / "session.jsonl")
    log.record(_verdict())
    assert len(log.events) == 1
    assert log.events[0]["flagged"] is True
    assert (tmp_path / "session.jsonl").read_text().count("\n") == 1


def test_export_reloads_to_same_events(tmp_path: Path) -> None:
    log = SessionLog(tmp_path / "session.jsonl")
    log.record(_verdict())
    dest = tmp_path / "out" / "export.jsonl"
    log.export(dest)
    reloaded = SessionLog.load(dest)
    assert reloaded == log.events
