"""Data structures describing PDF rendering options."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

PDF_STATE_KEY = "pdf_options"
PDF_FORMAT = "pdf"
MAX_CONTENT_INDEX = 2


class OutputFormat(str, Enum):
    """Response formats supported by the PDF renderer."""

    PDF = "pdf"


class PDFVariant(str, Enum):
    """Rendering variants exposed to clients."""

    A4 = "a4"
    A5 = "a5"
    A6 = "a6"
    A4_2UP = "a4-2up"
    A4_BOOKLET = "a4-booklet"
    A5_2UP = "a5-2up"
    A5_BOOKLET = "a5-booklet"


DEFAULT_VARIANT_CHOICE = PDFVariant.A4


@dataclass(frozen=True)
class PdfOptions:
    """Resolved request parameters for PDF generation."""

    requested: bool
    format_hint: OutputFormat | None = None
    variant: PDFVariant = DEFAULT_VARIANT_CHOICE
    index: int = 0
    custom_label: str | None = None

    def is_requested(self) -> bool:
        """Return True when the client explicitly asked for PDF output."""
        return bool(self.requested)


__all__ = [
    "DEFAULT_VARIANT_CHOICE",
    "MAX_CONTENT_INDEX",
    "PDFVariant",
    "OutputFormat",
    "PDF_FORMAT",
    "PDF_STATE_KEY",
    "PdfOptions",
]
