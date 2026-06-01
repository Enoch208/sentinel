from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import cast

import numpy as np

from sentinel_engine.types import Vector


@dataclass(frozen=True, slots=True)
class AnomalyRecord:
    frame_id: int
    ts: float
    zone: str
    vector: Vector


@dataclass(frozen=True, slots=True)
class AnomalyCluster:
    size: int
    exemplar_id: int
    zones: tuple[str, ...]
    first_ts: float
    last_ts: float


@dataclass(frozen=True, slots=True)
class WatchReport:
    total: int
    clusters: tuple[AnomalyCluster, ...]


def _cosine(a: Vector, b: Vector) -> float:
    norm = float(np.linalg.norm(a) * np.linalg.norm(b))
    if norm == 0.0:
        return 0.0
    return float(np.dot(a, b) / norm)


def cluster_anomalies(
    records: Sequence[AnomalyRecord], threshold: float = 0.85
) -> WatchReport:
    centroids: list[Vector] = []
    members: list[list[AnomalyRecord]] = []

    for record in records:
        match = -1
        best = threshold
        for index, centroid in enumerate(centroids):
            score = _cosine(record.vector, centroid)
            if score >= best:
                best = score
                match = index
        if match == -1:
            centroids.append(record.vector)
            members.append([record])
        else:
            members[match].append(record)
            stacked = np.stack([member.vector for member in members[match]])
            centroids[match] = cast(Vector, stacked.mean(axis=0).astype(np.float32))

    clusters = [
        AnomalyCluster(
            size=len(group),
            exemplar_id=group[0].frame_id,
            zones=tuple(sorted({member.zone for member in group})),
            first_ts=min(member.ts for member in group),
            last_ts=max(member.ts for member in group),
        )
        for group in members
    ]
    clusters.sort(key=lambda cluster: cluster.size, reverse=True)
    return WatchReport(total=len(records), clusters=tuple(clusters))
