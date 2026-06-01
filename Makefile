.DEFAULT_GOAL := help

.PHONY: help setup run demo test stop clean

help:
	@echo "Sentinel — make targets:"
	@echo "  make setup   install engine + desktop + frontend dependencies"
	@echo "  make run     launch the full instrument (engine + desktop app)"
	@echo "  make demo    headless demos: video anomaly, audio, precision/recall (no camera)"
	@echo "  make test    run every gate (engine pytest/ruff/mypy + desktop vitest/build)"
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

stop:
	pkill -f sentinel-serve || true

clean: stop
	rm -rf engine/sentinel.db engine/sessions /tmp/sentinel-demo.db
