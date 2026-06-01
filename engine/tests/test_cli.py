from __future__ import annotations

from sentinel_engine.cli import _render
from sentinel_engine.types import Verdict


def _verdict(
    *,
    score: float | None = 0.99,
    threshold: float = 0.90,
    flagged: bool = False,
    warming: bool = False,
) -> Verdict:
    return Verdict(
        frame_id=10,
        ts=10.0,
        score=score,
        threshold=threshold,
        flagged=flagged,
        warming=warming,
        neighbors=[],
    )


def test_render_warming() -> None:
    assert "learning normal" in _render(_verdict(warming=True, score=None))


def test_render_flagged_shows_score_and_threshold() -> None:
    out = _render(_verdict(flagged=True, score=0.5, threshold=0.9))
    assert "OUT OF PLACE" in out
    assert "0.500" in out
    assert "0.900" in out


def test_render_normal() -> None:
    out = _render(_verdict(score=0.99))
    assert "normal" in out
    assert "0.990" in out
