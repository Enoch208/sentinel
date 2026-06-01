from __future__ import annotations

from sentinel_engine.anomaly import AnomalyDetector


def test_warming_until_enough_history() -> None:
    detector = AnomalyDetector(warmup=5, window=20, sensitivity=0.5)
    assert detector.decide(0.9, point_count=2).warming is True


def test_flags_a_low_score_once_settled() -> None:
    detector = AnomalyDetector(warmup=5, window=20, sensitivity=0.5)
    for _ in range(10):
        detector.observe(0.95)
    settled = detector.decide(0.95, point_count=100)
    assert settled.warming is False
    assert settled.flagged is False
    assert detector.decide(0.50, point_count=100).flagged is True


def test_higher_sensitivity_raises_threshold() -> None:
    scores = [0.95, 0.80, 0.88, 0.70, 0.92, 0.78, 0.85, 0.90]

    low = AnomalyDetector(warmup=5, window=20, sensitivity=0.1)
    high = AnomalyDetector(warmup=5, window=20, sensitivity=0.9)
    for s in scores:
        low.observe(s)
        high.observe(s)

    t_low = low.decide(0.5, point_count=100).threshold
    t_high = high.decide(0.5, point_count=100).threshold
    assert t_high > t_low
