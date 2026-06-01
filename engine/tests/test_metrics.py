from __future__ import annotations

from sentinel_engine.metrics import footprint_mb


def test_footprint_is_positive() -> None:
    assert footprint_mb() > 0.0
