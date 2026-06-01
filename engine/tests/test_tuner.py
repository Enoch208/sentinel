from __future__ import annotations

from sentinel_engine.tuner import DeviceProfile, detect_profile, tune


def test_low_memory_enables_quantization() -> None:
    plan = tune(DeviceProfile(total_memory_mb=2048, cpu_cores=4))
    assert plan.quantize is True


def test_ample_memory_keeps_full_precision() -> None:
    plan = tune(DeviceProfile(total_memory_mb=32768, cpu_cores=10))
    assert plan.quantize is False


def test_fewer_cores_skip_more_frames() -> None:
    few = tune(DeviceProfile(total_memory_mb=8192, cpu_cores=2))
    many = tune(DeviceProfile(total_memory_mb=8192, cpu_cores=16))
    assert few.skip_hamming > many.skip_hamming


def test_tight_latency_lowers_hnsw_ef() -> None:
    tight = tune(
        DeviceProfile(total_memory_mb=8192, cpu_cores=8, latency_target_ms=120)
    )
    loose = tune(
        DeviceProfile(total_memory_mb=8192, cpu_cores=8, latency_target_ms=300)
    )
    assert tight.hnsw_ef < loose.hnsw_ef


def test_every_choice_has_a_rationale() -> None:
    plan = tune(DeviceProfile(total_memory_mb=4096, cpu_cores=4))
    assert plan.choices
    assert all(choice.rationale for choice in plan.choices)


def test_detect_profile_reports_real_values() -> None:
    profile = detect_profile()
    assert profile.total_memory_mb > 0.0
    assert profile.cpu_cores >= 1
