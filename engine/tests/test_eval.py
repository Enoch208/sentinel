from __future__ import annotations

from support import FakeEmbedder

from sentinel_engine.eval import evaluate_detection, run_synthetic_eval


def test_perfect_detection_scores_one() -> None:
    flags = [False, True, False, True]
    labels = [False, True, False, True]
    score = evaluate_detection(flags, labels)
    assert score.precision == 1.0
    assert score.recall == 1.0
    assert score.f1 == 1.0
    assert score.anomalies == 2


def test_false_positive_lowers_precision() -> None:
    score = evaluate_detection([True, True], [True, False])
    assert score.precision == 0.5
    assert score.recall == 1.0


def test_missed_anomaly_lowers_recall() -> None:
    score = evaluate_detection([False, False], [True, False])
    assert score.recall == 0.0


def test_mismatched_lengths_raise() -> None:
    import pytest

    with pytest.raises(ValueError):
        evaluate_detection([True], [True, False])


def test_synthetic_eval_recovers_the_injected_anomaly() -> None:
    score = run_synthetic_eval(FakeEmbedder(), total=60, anomaly_at=(40, 41, 42))
    assert score.anomalies == 3
    assert score.recall == 1.0
    assert score.precision == 1.0
