"""Shared PDF utilities for the backend."""

from .dependencies import get_pdf_options
from .options import PdfOptions
from .render import DEFAULT_VARIANT, VARIANT_SPECS, generate_pdf
from .route import PDFAwareRoute

__all__ = [
    "DEFAULT_VARIANT",
    "PDFAwareRoute",
    "PdfOptions",
    "VARIANT_SPECS",
    "generate_pdf",
    "get_pdf_options",
]
