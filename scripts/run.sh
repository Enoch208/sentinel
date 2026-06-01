#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENGINE="$ROOT/engine"
DESKTOP="$ROOT/desktop"
LOG="/tmp/sentinel-engine.log"
PORT=8765

require() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "✗ missing '$1' — install it first ($2)"
    exit 1
  }
}

require uv "https://docs.astral.sh/uv/"
require npm "https://nodejs.org"
require cargo "https://rustup.rs — needed by Tauri"

echo "▸ stopping any running Sentinel engine…"
pkill -f sentinel-serve 2>/dev/null || true
sleep 1

echo "▸ syncing engine dependencies…"
(cd "$ENGINE" && uv sync --quiet)

echo "▸ starting engine on ws://127.0.0.1:$PORT (log: $LOG)…"
(cd "$ENGINE" && uv run sentinel-serve) >"$LOG" 2>&1 &
ENGINE_PID=$!

cleanup() {
  echo ""
  echo "▸ shutting down engine…"
  kill "$ENGINE_PID" 2>/dev/null || true
  pkill -f sentinel-serve 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "▸ waiting for the engine to bind…"
for _ in $(seq 1 90); do
  if nc -z 127.0.0.1 "$PORT" 2>/dev/null; then
    break
  fi
  if ! kill -0 "$ENGINE_PID" 2>/dev/null; then
    echo "✗ engine exited early. Last log lines:"
    tail -20 "$LOG"
    exit 1
  fi
  sleep 1
done

if ! nc -z 127.0.0.1 "$PORT" 2>/dev/null; then
  echo "✗ engine did not bind within 90s. Last log lines:"
  tail -20 "$LOG"
  exit 1
fi

echo "✓ engine is up"
echo "▸ installing desktop dependencies (first run only)…"
(cd "$DESKTOP" && { [ -d node_modules ] || npm install; })

echo "▸ launching the desktop app — the first Rust build takes a few minutes."
echo "  grant camera permission when macOS asks."
(cd "$DESKTOP" && npm run tauri dev)
