# Sentinel

**An on-device, fully-offline perceptual instrument. It rides a camera, learns the "normal" of a space with embedded Qdrant, and flags in real time _what doesn't belong_ — then lets you explore that memory by example. No query box. No chatbot. No cloud.**

Built for the Qdrant "Think Outside the Bot" hackathon. Sentinel is the inverse of search: most edge-perception demos answer _"where is the thing I'm looking for?"_ — Sentinel answers the harder question an inspector, guard, or lab tech actually asks: _"what here is new, or out of place?"_ You can't query for the thing you didn't know to look for, so Sentinel doesn't make you. It watches, learns, and speaks once — when something breaks the pattern.

---

## How it works

```
camera ─▶ frame-skip (perceptual hash) ─▶ embed on-device (CLIP) ─▶ embedded Qdrant
                                                                          │
   new frame ─▶ nearest-neighbour query ─▶ below learned threshold? ─▶ ⚠ flag
                                                                          │
              teach 👍/👎 ─▶ reshape "normal"      explore ─▶ visual twins · zones · 2D map
```

The loop is **modality-agnostic at the vector level** — the same store + anomaly detector power both the camera and the microphone.

| Function | How |
|---|---|
| Learn "normal" | upsert kept-frame vectors into the `perceptions` collection |
| Anomaly check (per frame) | `query_points` nearest-neighbour; if top score < an adaptive rolling threshold ⇒ flag |
| Teach by example | 👍 adds the frame to normal memory; 👎 removes it (and records a negative) |
| Visual twins | dense nearest-neighbour over the memory (multivector-ready) |
| Zones | per-zone review via the Qdrant **Facet** API |
| Explore map | `scroll` vectors → **PCA** → 2D projection, anomalies highlighted |
| Watcher agent | online cosine clustering of recurring anomalies → end-of-walk report |

## Why embedded Qdrant (and Edge)

Sentinel runs Qdrant **in-process and fully offline** via the client's local mode (`QdrantClient(path=…)`) — no server, no network, persists to disk. This shares the **same points/Query API as Qdrant Edge**, so the code path drops onto Edge's `EdgeShard` with no change to the query logic when beta access lands. Edge is the production target; local mode is the honest, runs-anywhere build we ship today.

**Qdrant capabilities on the call path:** nearest-neighbour `query_points` (the hero anomaly loop + visual twins), the **Facet** API (per-zone anomaly review), `scroll` with vectors (the 2D explore map), and **scalar quantization** configured on the collection. `RecommendQuery` is implemented and tested as part of the teach/explore toolkit.

> **Honest note on quantization:** the in-process local engine does not apply scalar quantization (it's a pure-Python backend), so the dossier reports quantization as **off** there — savings only materialize on a real Qdrant Edge/server backend. Sentinel reports this truthfully rather than fabricating a number.

## Honest, live proof

Every figure in the dossier comes from the running engine, never hardcoded:

- **fps · embed ms · query ms · anomaly latency · process footprint · memory points · quantization state** — streamed live to the UI.
- `uv run sentinel-eval` — offline **detection precision/recall** on a staged scene (1.000 / 1.000 on the synthetic harness with the real CLIP model).
- `uv run sentinel-tune` — the engine **auto-tunes for the device** at launch (quantization / frame-skip / HNSW) with a stated rationale — the seam where **Qdrant Skills** would plug in.

## Principles (non-negotiable)

- **No box, no bot.** Every interaction is a gesture — Watch / Teach / Explore — never a typed query or chat.
- **Offline is the feature.** Kill the network mid-run and nothing changes.
- **Detection, not retrieval.** The headline is surfacing the unknown, deliberately not a "find my keys" clone.
- **Honest metrics.** The dossier reflects the real engine, trade-offs and all.

## Run it (offline)

**One command** (needs `uv`, `npm`, and `cargo`):

```bash
make setup    # first time: install all dependencies
make run      # stops any stale engine, starts it, waits for it, opens the app
make demo     # headless: video anomaly + audio + precision/recall (no camera)
make test     # every gate: engine pytest/ruff/mypy + desktop vitest/build
```

`make run` launches the engine, waits until it actually binds `ws://127.0.0.1:8765`, then opens the desktop app and cleans up the engine on exit. Grant camera permission when macOS asks. The first `tauri dev` compiles the Rust shell (a few minutes).

<details>
<summary>Or run the two processes by hand</summary>

**Engine** — Python 3.12 via [`uv`](https://docs.astral.sh/uv/) (the ML wheels lag newer Python; the engine pins 3.12):

```bash
cd engine
uv sync
uv run sentinel --synthetic     # headless demo: learns normal, flags an injected anomaly
uv run sentinel-audio           # multimodal: flags an out-of-place sound
uv run sentinel-eval            # detection precision/recall on a staged scene
uv run sentinel-tune            # device-aware auto-tuning plan
uv run sentinel-serve           # WebSocket server on ws://127.0.0.1:8765 for the desktop shell
uv run sentinel                 # live webcam (grant the terminal camera permission)
```

**Desktop shell** — Tauri 2 + React (connects to the engine over WebSocket):

```bash
cd desktop
npm install
npm run tauri dev
```

</details>

Point the camera at a scene → it learns "normal" → introduce something out of place → the view glows amber with **⚠ out of place** → switch to Teach and hit 👍 to suppress it → open Explore for visual twins, per-zone facets, the watcher's end-of-walk report, and the 2D memory map → **turn off wifi; it keeps working.**

## Layout

| Path | What |
|---|---|
| `engine/` | Python perception engine — capture, embed, embedded Qdrant, anomaly loop, teach, twins, zones, audio, watcher, explore map, auto-tuner, FastAPI WebSocket server |
| `desktop/` | Tauri 2 desktop shell (React + TS + Vite) — live view, overlay, guided tour, dossier, Explore |
| `frontend/` | Marketing/landing site (Next.js 16) |

## Tests

```bash
cd engine && uv run pytest && uv run ruff check . && uv run mypy src tests
cd desktop && npm run test && npm run build
```

The engine suite runs with no camera, model download, or network (fakes + synthetic scenes). The desktop suite covers the view-state logic and the engine socket hook.

## Built with

- [Qdrant](https://qdrant.tech) — embedded vector engine (architected for Qdrant Edge)
- [FastEmbed](https://github.com/qdrant/fastembed) — on-device CLIP image embeddings (`Qdrant/clip-ViT-B-32-vision`)
- [OpenCV](https://opencv.org) — webcam capture · [NumPy](https://numpy.org) — spectral audio features & PCA
- [FastAPI](https://fastapi.tiangolo.com) · [Tauri](https://tauri.app) · [React](https://react.dev) · [Vite](https://vite.dev)

## Status

The instrument is feature-complete across the planned P0–P2 surface and fully tested headlessly. The live webcam/microphone paths and the `tauri dev` window require local hardware/permissions to exercise. Qdrant Edge is private beta; Sentinel is built to swap onto `EdgeShard` when access lands, and does not overclaim it today.
