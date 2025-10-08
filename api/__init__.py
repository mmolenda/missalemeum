"""Compatibility package exposing `backend.api` as `api`.

This keeps existing imports like `from api.app import app` working while the
actual implementation lives under `backend/api`.
"""
from __future__ import annotations

import sys
from pathlib import Path

_CURRENT_DIR = Path(__file__).resolve().parent
_BACKEND_API_DIR = _CURRENT_DIR.parent / "backend" / "api"

if not _BACKEND_API_DIR.exists():
    raise ImportError(f"backend.api package not found at {_BACKEND_API_DIR}")

_BACKEND_DIR = _BACKEND_API_DIR.parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

__path__ = [str(_BACKEND_API_DIR)]

