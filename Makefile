.DEFAULT_GOAL := help

.PHONY: help setup run qdrant run-server demo test stop clean pack-engine dmg release

help:
	@echo "Sentinel — make targets:"
	@echo "  make setup   install engine + desktop + frontend dependencies"
	@echo "  make run         launch the full instrument (engine + desktop app)"
	@echo "  make run-server  launch with a real Qdrant (Docker) — quantization genuinely on"
	@echo "  make demo    headless demos: video anomaly, audio, precision/recall (no camera)"
	@echo "  make test    run every gate (engine pytest/ruff/mypy + desktop vitest/build)"
	@echo "  make dmg     build a standalone macOS .app/.dmg (bundles engine + model)"
	@echo "  make release publish the built .dmg as a GitHub release (needs gh)"
	@echo "  make stop    stop the running engine"
	@echo "  make clean   stop the engine and wipe the local memory database"

setup:
	cd engine && uv sync
	cd desktop && npm install
	cd frontend && npm install

run:
	bash scripts/run.sh

qdrant:
	@docker start sentinel-qdrant >/dev/null 2>&1 || docker run -d --name sentinel-qdrant -p 6333:6333 qdrant/qdrant >/dev/null
	@for i in $$(seq 1 30); do nc -z 127.0.0.1 6333 2>/dev/null && break; sleep 1; done

run-server: qdrant
	SENTINEL_QDRANT_URL=http://127.0.0.1:6333 SENTINEL_QUANTIZE=1 bash scripts/run.sh

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

release:
	@dmg=$$(ls desktop/src-tauri/target/release/bundle/dmg/*.dmg 2>/dev/null | head -1); \
	if [ -z "$$dmg" ]; then echo "no .dmg found — run 'make dmg' first"; exit 1; fi; \
	echo "releasing $$dmg"; \
	gh release create v0.1.0 --title "Sentinel v0.1.0" \
	  --notes "On-device, offline anomaly detection for macOS (Apple Silicon). Unsigned: right-click the app and choose Open on first launch." 2>/dev/null || true; \
	gh release upload v0.1.0 "$$dmg" --clobber

stop:
	pkill -f sentinel-serve || true
	docker stop sentinel-qdrant 2>/dev/null || true

clean: stop
	rm -rf engine/sentinel.db engine/sessions /tmp/sentinel-demo.db
