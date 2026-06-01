from __future__ import annotations

import numpy as np

from sentinel_engine.capture import SyntheticScene


def test_yields_requested_frame_count_with_sequential_ids() -> None:
    scene = SyntheticScene(total=10, anomaly_at=(5,))
    frames = list(scene.frames())
    assert len(frames) == 10
    assert [f.id for f in frames] == list(range(10))


def test_anomaly_frame_differs_far_more_than_normal_jitter() -> None:
    scene = SyntheticScene(total=10, anomaly_at=(5,))
    images = {f.id: f.image.astype(np.int32) for f in scene.frames()}

    normal_jitter = np.abs(images[4] - images[3]).mean()
    anomaly_delta = np.abs(images[5] - images[4]).mean()
    assert anomaly_delta > normal_jitter * 5
