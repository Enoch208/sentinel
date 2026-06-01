.DEFAULT_GOAL := help

.PHONY: help setup run demo test stop clean pack-engine dmg

help:
	@echo "Sentinel — make targets:"
	@echo "  make setup   install engine + desktop + frontend dependencies"
	@echo "  make run     launch the full instrument (engine + desktop app)"
	@echo "  make demo    headless demos: video anomaly, audio, precision/recall (no camera)"
	@echo "  make test    run every gate (engine pytest/ruff/mypy + desktop vitest/build)"
	@echo "  make dmg     build a standalone macOS .app/.dmg (bundles engine + model)"
	@echo "  make stop    stop the running engine"
	@echo "  make clean   stop the engine and wipe the local memory database"

setup:
	cd engine && uv sync
	cd desktop && npm install
	cd frontend && npm install

run:
	bash scripts/run.sh

demo:
	cd engine && uv run sentinel --synthetic --db /tmp/sentinel-demo.db && uv run sentinel-audio && uv run sentinel-eval

test:
	cd engine && uv run ruff check . && uv run mypy src tests && uv run pytest
	cd desktop && npm run test && npm run build

pack-engine:
	cd engine && uv run pyinstaller --onedir --name sentinel-serve --noconfirm \
	  --collect-all fastembed --collect-all onnxruntime --collect-all qdrant_client \
	  --collect-all cv2 --collect-all tokenizers --collect-all pydantic \
	  packaging/serve_entry.py

dmg: pack-engine
	rm -rf desktop/src-tauri/resources/engine/* desktop/src-tauri/resources/model/*
	cp -R engine/dist/sentinel-serve/. desktop/src-tauri/resources/engine/
	cp -R engine/.fastembed_cache/. desktop/src-tauri/resources/model/
	cd desktop && npm run tauri build

stop:
	pkill -f sentinel-serve || true

clean: stop
	rm -rf engine/sentinel.db engine/sessions /tmp/sentinel-demo.db
