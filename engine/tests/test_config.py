from __future__ import annotations

import pytest

from sentinel_engine.config import Settings, apply_env_overrides


def test_env_overrides_db_and_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SENTINEL_DB", "/tmp/custom.db")
    monkeypatch.setenv("SENTINEL_CACHE", "/tmp/models")
    monkeypatch.setenv("SENTINEL_QDRANT_URL", "http://localhost:6333")
    monkeypatch.setenv("SENTINEL_QUANTIZE", "0")
    settings = apply_env_overrides(Settings())
    assert settings.db_path == "/tmp/custom.db"
    assert settings.cache_dir == "/tmp/models"
    assert settings.qdrant_url == "http://localhost:6333"
    assert settings.quantize is False


def test_no_env_keeps_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SENTINEL_DB", raising=False)
    monkeypatch.delenv("SENTINEL_CACHE", raising=False)
    monkeypatch.delenv("SENTINEL_QDRANT_URL", raising=False)
    monkeypatch.delenv("SENTINEL_QUANTIZE", raising=False)
    defaults = Settings()
    settings = apply_env_overrides(Settings())
    assert settings.db_path == defaults.db_path
    assert settings.cache_dir == defaults.cache_dir
    assert settings.qdrant_url == defaults.qdrant_url
    assert settings.quantize == defaults.quantize
