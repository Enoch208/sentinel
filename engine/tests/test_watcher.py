from __future__ import annotations

import numpy as np

from sentinel_engine.watcher import AnomalyRecord, cluster_anomalies


def _record(frame_id: int, vector: list[float], zone: str = "default") -> AnomalyRecord:
    return AnomalyRecord(
        frame_id=frame_id,
        ts=float(frame_id),
        zone=zone,
        vector=np.array(vector, dtype=np.float32),
    )


def test_empty_report() -> None:
    report = cluster_anomalies([])
    assert report.total == 0
    assert report.clusters == ()


def test_groups_similar_anomalies_into_clusters() -> None:
    records = [
        _record(1, [1, 0, 0, 0]),
        _record(2, [0.99, 0.01, 0, 0]),
        _record(3, [0, 1, 0, 0], zone="shelf"),
        _record(4, [0.02, 0.98, 0, 0], zone="shelf"),
    ]
    report = cluster_anomalies(records, threshold=0.9)

    assert report.total == 4
    assert len(report.clusters) == 2
    assert {cluster.size for cluster in report.clusters} == {2}


def test_clusters_sorted_by_size_descending() -> None:
    records = [
        _record(1, [1, 0, 0, 0]),
        _record(2, [1, 0, 0, 0]),
        _record(3, [1, 0, 0, 0]),
        _record(4, [0, 1, 0, 0]),
    ]
    report = cluster_anomalies(records, threshold=0.9)

    assert [cluster.size for cluster in report.clusters] == [3, 1]
    assert report.clusters[0].exemplar_id == 1
