"""Temporary PDF generation stub.

For now, returns a static resource while the real PDF formatting is implemented.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi.responses import FileResponse

RESOURCES_DIR = Path(__file__).resolve().parents[2] / "resources"
STATIC_PDF_NAME = "proper.pdf"


def generate_pdf(*, payload: Any, variant: str, format_hint: str) -> FileResponse:
    """Return a static PDF placeholder for endpoints requesting PDF output."""
    pdf_path = RESOURCES_DIR / STATIC_PDF_NAME
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=STATIC_PDF_NAME,
    )
