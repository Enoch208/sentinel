# Sentinel Engine

The on-device perceptual instrument: capture webcam frames, skip redundant ones, embed each kept frame locally, store and query an embedded Qdrant memory, and flag in real time what doesn't belong. Fully offline, in-process.

See `../docs/superpowers/specs/2026-06-01-sentinel-engine-design.md` for the design.

## Setup

```bash
uv sync
```

## Run the headless loop

```bash
uv run sentinel              # live webcam
uv run sentinel --synthetic  # no camera; generated frames + an injected anomaly
```

## Develop

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```
