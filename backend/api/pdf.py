"""Utilities for PDF-enabled endpoints."""
from __future__ import annotations

from typing import Any, Callable, TypeVar

PDF_AVAILABLE_ATTR = "_pdf_downloadable"

F = TypeVar("F", bound=Callable[..., Any])


def pdf_downloadable(func: F) -> F:
    """Mark a FastAPI endpoint as supporting PDF downloads."""
    setattr(func, PDF_AVAILABLE_ATTR, True)
    return func


def is_pdf_downloadable(endpoint: Any) -> bool:
    """Check if an endpoint has been marked as supporting PDF downloads."""
    return bool(getattr(endpoint, PDF_AVAILABLE_ATTR, False))
