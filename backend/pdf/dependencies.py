"""Dependencies exposing PDF rendering options via OpenAPI."""
from __future__ import annotations

from fastapi import Query, Request

from .options import (
    DEFAULT_VARIANT_CHOICE,
    MAX_CONTENT_INDEX,
    OutputFormat,
    PDF_STATE_KEY,
    PDFVariant,
    PdfOptions,
)


def _accepts_pdf(request: Request) -> bool:
    accept_header = request.headers.get("accept", "")
    return "application/pdf" in accept_header.lower()


def _clamp_index(value: int | None) -> int:
    if value is None:
        return 0
    if value < 0 or value > MAX_CONTENT_INDEX:
        return 0
    return value


async def get_pdf_options(
    request: Request,
    format_: OutputFormat | None = Query(
        default=None,
        alias="format",
        description="Set to `pdf` to request the response as a PDF document.",
    ),
    variant: PDFVariant = Query(
        default=DEFAULT_VARIANT_CHOICE,
        description="Page layout variant to use when rendering the PDF. 2up - 2 pages on one sheet. Booklet - pages on one sheet, foldable.",
    ),
    index: int = Query(
        default=0,
        ge=0,
        le=MAX_CONTENT_INDEX,
        description="Select the Mass from the day, if there's more than one (for example All Souls).",
    ),
    custom_label: str | None = Query(
        default=None,
        description="Optional custom label added to the PDF metadata and header.",
    ),
) -> PdfOptions:
    """Resolve PDF rendering options for endpoints that opt into PDF support."""

    format_choice = format_
    requested = False

    if format_choice is not None:
        requested = format_choice == OutputFormat.PDF
    elif _accepts_pdf(request):
        format_choice = OutputFormat.PDF
        requested = True

    clamped_index = _clamp_index(index)

    options = PdfOptions(
        requested=requested,
        format_hint=format_choice,
        variant=variant,
        index=clamped_index,
        custom_label=custom_label,
    )

    setattr(request.state, PDF_STATE_KEY, options)
    return options

__all__ = ["get_pdf_options"]
