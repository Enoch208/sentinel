from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeviceProfile:
    total_memory_mb: float
    cpu_cores: int
    latency_target_ms: float = 200.0


@dataclass(frozen=True, slots=True)
class TuningChoice:
    setting: str
    value: str
    rationale: str


@dataclass(frozen=True, slots=True)
class TuningPlan:
    quantize: bool
    skip_hamming: int
    sensitivity: float
    hnsw_ef: int
    choices: tuple[TuningChoice, ...]


def detect_profile(latency_target_ms: float = 200.0) -> DeviceProfile:
    cores = os.cpu_count() or 1
    try:
        total = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
        memory_mb = total / (1024.0 * 1024.0)
    except (ValueError, OSError, AttributeError):
        memory_mb = 4096.0
    return DeviceProfile(
        total_memory_mb=memory_mb,
        cpu_cores=cores,
        latency_target_ms=latency_target_ms,
    )


def tune(profile: DeviceProfile) -> TuningPlan:
    gb = profile.total_memory_mb / 1024.0
    quantize = profile.total_memory_mb < 8192.0
    quant_reason = (
        f"{gb:.1f} GB RAM — int8 scalar quantization (~4x smaller vectors) to fit "
        "the edge memory budget"
        if quantize
        else f"{gb:.1f} GB RAM — ample memory, keep full precision for best recall"
    )

    if profile.cpu_cores <= 4:
        skip = 12
        skip_reason = (
            f"{profile.cpu_cores} cores — skip near-duplicate frames aggressively "
            "to hold real-time embedding"
        )
    elif profile.cpu_cores <= 8:
        skip = 8
        skip_reason = f"{profile.cpu_cores} cores — balanced frame-skip"
    else:
        skip = 4
        skip_reason = f"{profile.cpu_cores} cores — light frame-skip, headroom to embed"

    tight = profile.latency_target_ms <= 150.0
    hnsw_ef = 64 if tight else 128
    ef_reason = (
        f"{profile.latency_target_ms:.0f} ms target — smaller ef for faster queries"
        if tight
        else f"{profile.latency_target_ms:.0f} ms target — larger ef for higher recall"
    )

    return TuningPlan(
        quantize=quantize,
        skip_hamming=skip,
        sensitivity=0.5,
        hnsw_ef=hnsw_ef,
        choices=(
            TuningChoice("quantization", "int8" if quantize else "off", quant_reason),
            TuningChoice("frame_skip_hamming", str(skip), skip_reason),
            TuningChoice("hnsw_ef", str(hnsw_ef), ef_reason),
        ),
    )


def main() -> int:
    profile = detect_profile()
    plan = tune(profile)
    print(
        f"device: {profile.total_memory_mb / 1024:.1f} GB RAM · "
        f"{profile.cpu_cores} cores · target {profile.latency_target_ms:.0f} ms"
    )
    print("auto-tuned engine settings (Qdrant Skills-style):")
    for choice in plan.choices:
        print(f"  {choice.setting} = {choice.value}  — {choice.rationale}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
