from __future__ import annotations

import pytest

from sentinel_engine.embed import FastEmbedImageEmbedder


def test_unknown_model_raises_before_any_download() -> None:
    with pytest.raises(ValueError):
        FastEmbedImageEmbedder("definitely/not-a-real-model")
