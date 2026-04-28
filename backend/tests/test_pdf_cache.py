from __future__ import annotations

import importlib
from pathlib import Path


def _reload_pdf_common(monkeypatch, cache_dir: Path | None):
    if cache_dir is None:
        monkeypatch.delenv("PDF_CACHE_DIR", raising=False)
    else:
        monkeypatch.setenv("PDF_CACHE_DIR", str(cache_dir))

    import pdf.common as common

    existing_cache = getattr(common, "cache", None)
    if hasattr(existing_cache, "close"):
        existing_cache.close()

    return importlib.reload(common)


def test_pdf_cache_disabled_without_cache_dir(monkeypatch):
    common = _reload_pdf_common(monkeypatch, None)

    assert isinstance(common.cache, common.NoCache)


def test_pdf_cache_disabled_for_group_writable_dir(monkeypatch, tmp_path):
    cache_dir = tmp_path / "pdf-cache"
    cache_dir.mkdir(mode=0o777)
    cache_dir.chmod(0o777)

    common = _reload_pdf_common(monkeypatch, cache_dir)

    assert isinstance(common.cache, common.NoCache)


def test_pdf_cache_enabled_for_owner_only_dir(monkeypatch, tmp_path):
    cache_dir = tmp_path / "pdf-cache"
    cache_dir.mkdir(mode=0o700)
    cache_dir.chmod(0o700)

    common = _reload_pdf_common(monkeypatch, cache_dir)

    try:
        assert not isinstance(common.cache, common.NoCache)
        common.cache.set("smoke", "ok", expire=None)
        assert common.cache.get("smoke") == "ok"
    finally:
        common.cache.close()
