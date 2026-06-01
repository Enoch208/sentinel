from __future__ import annotations

import numpy as np

from sentinel_engine.frameskip import FrameGate


def _gradient() -> np.ndarray:
    ramp = np.tile(np.linspace(0, 255, 64, dtype=np.uint8), (64, 1))
    return np.stack([ramp, ramp, ramp], axis=2)


def test_keeps_first_skips_duplicate() -> None:
    gate = FrameGate(hamming_threshold=8)
    image = _gradient()
    assert gate.should_keep(image) is True
    assert gate.should_keep(image.copy()) is False


def test_keeps_a_clearly_different_frame() -> None:
    gate = FrameGate(hamming_threshold=8)
    rng = np.random.default_rng(0)
    noisy = rng.integers(0, 256, (64, 64, 3), dtype=np.uint8)
    assert gate.should_keep(_gradient()) is True
    assert gate.should_keep(noisy) is True


def test_counts_seen_and_kept() -> None:
    gate = FrameGate(hamming_threshold=8)
    image = _gradient()
    gate.should_keep(image)
    gate.should_keep(image.copy())
    assert gate.seen == 2
    assert gate.kept == 1
