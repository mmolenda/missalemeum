"""Temporary PDF generation stub.

For now, returns a static resource while the real PDF formatting is implemented.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi.responses import FileResponse
from weasyprint import HTML

RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"
STATIC_PDF_NAME = "proper.pdf"


def generate_pdf(*, payload: Any, variant: str, format_hint: str) -> FileResponse:
    """Return a static PDF placeholder for endpoints requesting PDF output."""
    filename = "/tmp/document.pdf"
    HTML(string=f"<h1>{payload[0]['info']['title']}</h1><p>{payload[0]['info']['description']}</p><h2>{payload[0]['sections'][1]['label']}</h2><p>{[payload[0]['sections'][1]['body'][0][0]]}</p>").write_pdf(filename, pdf_variant="pdf/a-3u")
    return FileResponse(
        path=filename,
        media_type="application/pdf",
        filename=STATIC_PDF_NAME,
    )
