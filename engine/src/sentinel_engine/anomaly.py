from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from statistics import fmean, pstdev


@dataclass(frozen=True, slots=True)
class Decision:
    flagged: bool
    threshold: float
    warming: bool


class AnomalyDetector:
    def __init__(
        self,
        warmup: int,
        window: int,
        sensitivity: float,
        margin: float = 0.05,
    ) -> None:
        self._warmup = warmup
        self._scores: deque[float] = deque(maxlen=window)
        self._sensitivity = _clamp(sensitivity)
        self._margin = margin

    @property
    def sensitivity(self) -> float:
        return self._sensitivity

    def set_sensitivity(self, value: float) -> None:
        self._sensitivity = _clamp(value)

    def observe(self, top_score: float) -> None:
        self._scores.append(top_score)

    def decide(self, top_score: float | None, point_count: int) -> Decision:
        if (
            top_score is None
            or point_count < self._warmup
            or len(self._scores) < self._warmup
        ):
            return Decision(flagged=False, threshold=0.0, warming=True)
        mean = fmean(self._scores)
        spread = pstdev(self._scores)
        z = 3.0 - 2.0 * self._sensitivity
        gap = max(z * spread, self._margin)
        threshold = min(1.0, max(0.0, mean - gap))
        return Decision(
            flagged=top_score < threshold, threshold=threshold, warming=False
        )


def _clamp(value: float) -> float:
    return min(1.0, max(0.0, value))
