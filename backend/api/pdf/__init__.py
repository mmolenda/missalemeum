"""PDF support utilities."""
from __future__ import annotations

from .decorators import is_pdf_downloadable, pdf_downloadable
from .middleware import PDFDownloadMiddleware

__all__ = [
    "pdf_downloadable",
    "is_pdf_downloadable",
    "PDFDownloadMiddleware",
]
