"""Shared utilities for generating printable PDFs."""
from __future__ import annotations

import logging
import os
import re
import unicodedata
from dataclasses import dataclass
from html import escape
from io import BytesIO
from types import ModuleType
import mistune
from diskcache import Cache
from pypdf import PageObject, PdfReader, PdfWriter, Transformation
from pypdf.generic import DecodedStreamObject, NameObject
from weasyprint import HTML

from api.constants import TRANSLATION

from .styles import build_bilingual_print_styles


log = logging.getLogger(__name__)

DEFAULT_CACHE_SIZE_BYTES = int(1e9)


def _resolve_cache_size(raw_value: str | None) -> int:
    if raw_value is None:
        return DEFAULT_CACHE_SIZE_BYTES
    try:
        return int(raw_value)
    except ValueError:
        log.warning(
            "Invalid PDF_CACHE_SIZE_BYTES=%r; falling back to default %d",
            raw_value,
            DEFAULT_CACHE_SIZE_BYTES,
        )
        return DEFAULT_CACHE_SIZE_BYTES


class NoCache:
    def __contains__(self, key): return False
    def get(self, key, default=None): return default
    def set(self, key, value, expire=None): pass


if cache_dir := os.getenv("PDF_CACHE_DIR"):
    cache_size_limit = _resolve_cache_size(os.getenv("PDF_CACHE_SIZE_BYTES"))
    cache = Cache(cache_dir, size_limit=cache_size_limit)
    log.info(
        "PDF cache enabled at %s with size limit %d bytes",
        cache_dir,
        cache_size_limit,
    )
else:
    cache = NoCache()
    log.info("PDF cache disabled (PDF_CACHE_DIR not set)")


MM_TO_PT = 72 / 25.4
PAGE_DIMENSIONS_MM: dict[str, tuple[float, float]] = {
    "A4": (210.0, 297.0),
    "A5": (148.0, 210.0),
    "A6": (105.0, 148.0),
    "HALF_LETTER": (139.7, 215.9),
    "LETTER": (215.9, 279.4),
}


@dataclass(frozen=True)
class VariantSpec:
    """Rendering configuration for the supported PDF variants."""

    page_size: str
    font_scale: float
    mode: str = "normal"  # normal | two_up | booklet
    sheet_size: str | None = None


VARIANT_SPECS: dict[str, VariantSpec] = {
    "a4": VariantSpec(page_size="A4", font_scale=1.0),
    "a5": VariantSpec(page_size="A5", font_scale=0.9),
    "a6": VariantSpec(page_size="A6", font_scale=0.8),
    "a4-2up": VariantSpec(page_size="A5", font_scale=0.9, mode="two_up", sheet_size="A4"),
    "a4-booklet": VariantSpec(page_size="A5", font_scale=0.9, mode="booklet", sheet_size="A4"),
    "a5-2up": VariantSpec(page_size="A6", font_scale=0.8, mode="two_up", sheet_size="A5"),
    "a5-booklet": VariantSpec(page_size="A6", font_scale=0.8, mode="booklet", sheet_size="A5"),
    "letter": VariantSpec(page_size="LETTER", font_scale=1.0),
    "letter-2up": VariantSpec(page_size="HALF_LETTER", font_scale=0.9, mode="two_up", sheet_size="LETTER"),
    "letter-booklet": VariantSpec(page_size="HALF_LETTER", font_scale=0.9, mode="booklet", sheet_size="LETTER"),
}
DEFAULT_VARIANT = VARIANT_SPECS["a4"]
DEFAULT_LANGUAGE = "en"
SITE_LABEL = "www.missalemeum.com"

_MARKDOWN = mistune.create_markdown(
    escape=False,
    plugins=("strikethrough", "table", "task_lists", "footnotes", "abbr"),
)


@dataclass
class RenderedContent:
    filename: str
    pdf_bytes: bytes


def _get_translation_module(lang: str) -> tuple[ModuleType, str]:
    if lang in TRANSLATION:
        return TRANSLATION[lang], lang
    if DEFAULT_LANGUAGE in TRANSLATION:
        return TRANSLATION[DEFAULT_LANGUAGE], DEFAULT_LANGUAGE
    # Fallback to any available translation module
    fallback_lang, module = next(iter(TRANSLATION.items()))
    return module, fallback_lang


def _wrap_html(body_html: str, *, page_size: str, font_scale: float, title: str, lang: str) -> str:
    translation, resolved_lang = _get_translation_module(lang)
    labels = getattr(translation, "PDF_LABELS", {})
    if not isinstance(labels, dict):
        labels = {}
    css = build_bilingual_print_styles(
        page_size=page_size,
        font_scale=font_scale,
        site_label=SITE_LABEL,
    )
    lang_attr = escape(resolved_lang or DEFAULT_LANGUAGE)
    return (
        "<!DOCTYPE html>"
        f"<html lang=\"{lang_attr}\">"
        "<head>"
        "<meta charset=\"utf-8\"/>"
        f"<title>{escape(title)}</title>"
        f"<style>{css}</style>"
        "</head>"
        "<body class=\"print-body\">"
        f"{body_html}"
        "</body></html>"
    )


def _render_markdown(text: str, *, markdown_newlines: bool | None = None) -> str:
    if markdown_newlines is None:
        markdown_newlines = False

    if markdown_newlines:
        text = text.replace("\n", "  \n")
    return _MARKDOWN(text)


def _page_dimensions(size: str, *, orientation: str = "portrait") -> tuple[float, float]:
    width_mm, height_mm = PAGE_DIMENSIONS_MM.get(size.upper(), PAGE_DIMENSIONS_MM[size])
    if orientation == "landscape":
        width_mm, height_mm = height_mm, width_mm
    return width_mm * MM_TO_PT, height_mm * MM_TO_PT


def _add_fold_markers(page: PageObject, sheet_width: float, sheet_height: float) -> None:
    """Draw subtle folding markers down the centre of imposed booklet sheets."""

    center_x = sheet_width / 2
    center_y = sheet_height / 2

    cross_half = min(sheet_width, sheet_height) * 0.03
    cross_half = max(12.0, min(cross_half, 24.0))

    gutter_extension = 10.0
    edge_offset = 18.0
    edge_half = 6.0

    target_length = min(gutter_extension, edge_half * 2)
    if target_length <= 0:
        target_length = 8.0
    cross_half = target_length / 2
    gutter_extension = target_length
    edge_half = target_length / 2

    instructions = (
        "q\n"
        "0.9 0.9 0.9 RG\n"
        "1 w\n"
        f"{center_x:.2f} {center_y - cross_half:.2f} m {center_x:.2f} {center_y + cross_half:.2f} l S\n"
        f"{center_x - cross_half:.2f} {center_y:.2f} m {center_x + cross_half:.2f} {center_y:.2f} l S\n"
        f"{center_x:.2f} {sheet_height - edge_offset:.2f} m {center_x:.2f} {sheet_height - edge_offset - gutter_extension:.2f} l S\n"
        f"{center_x - edge_half:.2f} {sheet_height - edge_offset:.2f} m {center_x + edge_half:.2f} {sheet_height - edge_offset:.2f} l S\n"
        f"{center_x:.2f} {edge_offset:.2f} m {center_x:.2f} {edge_offset + gutter_extension:.2f} l S\n"
        f"{center_x - edge_half:.2f} {edge_offset:.2f} m {center_x + edge_half:.2f} {edge_offset:.2f} l S\n"
        "Q\n"
    )
    overlay_writer = PdfWriter()
    overlay_page = overlay_writer.add_blank_page(width=sheet_width, height=sheet_height)
    stream = DecodedStreamObject()
    stream.set_data(instructions.encode("ascii"))
    overlay_page[NameObject("/Contents")] = overlay_writer._add_object(stream)

    buffer = BytesIO()
    overlay_writer.write(buffer)
    buffer.seek(0)
    overlay_reader = PdfReader(buffer)
    page.merge_page(overlay_reader.pages[0])


def _merge_page_into_slot(
    destination: PageObject,
    source: PageObject,
    slot_width: float,
    slot_height: float,
    *,
    offset_x: float,
) -> None:
    src_width = float(source.mediabox.width)
    src_height = float(source.mediabox.height)

    scale = min(slot_width / src_width, slot_height / src_height)
    scaled_width = src_width * scale
    scaled_height = src_height * scale

    translate_x = offset_x + (slot_width - scaled_width) / 2
    translate_y = (slot_height - scaled_height) / 2

    transformation = Transformation().scale(scale).translate(translate_x, translate_y)
    destination.merge_transformed_page(source, transformation, expand=False)


def _impose_two_up(pdf_bytes: bytes, sheet_size: str) -> bytes:
    reader = PdfReader(BytesIO(pdf_bytes))
    writer = PdfWriter()

    sheet_width, sheet_height = _page_dimensions(sheet_size, orientation="landscape")

    slot_width = sheet_width / 2
    pages = list(reader.pages)

    for index in range(0, len(pages), 2):
        left_page = pages[index]
        right_page = pages[index + 1] if index + 1 < len(pages) else None

        imposed_page = PageObject.create_blank_page(None, width=sheet_width, height=sheet_height)
        _merge_page_into_slot(imposed_page, left_page, slot_width, sheet_height, offset_x=0)
        if right_page is not None:
            _merge_page_into_slot(imposed_page, right_page, slot_width, sheet_height, offset_x=slot_width)
        added = writer.add_page(imposed_page)
        added.compress_content_streams()

    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def _impose_booklet(pdf_bytes: bytes, sheet_size: str) -> bytes:
    reader = PdfReader(BytesIO(pdf_bytes))
    writer = PdfWriter()

    sheet_width, sheet_height = _page_dimensions(sheet_size, orientation="landscape")
    slot_width = sheet_width / 2
    pages = list(reader.pages)
    total = len(pages)

    even_total = total if total % 4 == 0 else ((total // 4) + 1) * 4
    blank_pages_needed = even_total - total

    for _ in range(blank_pages_needed):
        pages.append(PageObject.create_blank_page(None, width=pages[0].mediabox.width, height=pages[0].mediabox.height))

    left_index = len(pages) - 1
    right_index = 0

    while right_index < left_index:
        front_page = PageObject.create_blank_page(None, width=sheet_width, height=sheet_height)
        _merge_page_into_slot(front_page, pages[left_index], slot_width, sheet_height, offset_x=0)
        _merge_page_into_slot(front_page, pages[right_index], slot_width, sheet_height, offset_x=slot_width)
        _add_fold_markers(front_page, sheet_width, sheet_height)
        added_front = writer.add_page(front_page)
        added_front.compress_content_streams()
        right_index += 1
        left_index -= 1

        if right_index > left_index:
            break

        back_page = PageObject.create_blank_page(None, width=sheet_width, height=sheet_height)
        _merge_page_into_slot(back_page, pages[right_index], slot_width, sheet_height, offset_x=0)
        _merge_page_into_slot(back_page, pages[left_index], slot_width, sheet_height, offset_x=slot_width)
        _add_fold_markers(back_page, sheet_width, sheet_height)
        added_back = writer.add_page(back_page)
        added_back.compress_content_streams()
        right_index += 1
        left_index -= 1

    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def _render_base_pdf(html_document: str) -> bytes:
    return HTML(string=html_document).write_pdf()


def _apply_variant(base_pdf_bytes: bytes, spec: VariantSpec) -> bytes:
    if spec.mode == "two_up":
        sheet_size = spec.sheet_size or "A4"
        return _impose_two_up(base_pdf_bytes, sheet_size)
    if spec.mode == "booklet":
        sheet_size = spec.sheet_size or "A4"
        return _impose_booklet(base_pdf_bytes, sheet_size)
    return base_pdf_bytes


def _slugify_for_filename(value: str) -> str:
    if not value:
        return "missale-meum"
    # Normalize and strip accents
    normalized = unicodedata.normalize("NFKD", value)
    stripped = "".join(
        c for c in normalized if not unicodedata.combining(c)
    )
    # Polish special case (ł isn’t decomposed by NFKD)
    stripped = stripped.replace("ł", "l").replace("Ł", "L")
    # Encode to ASCII safely
    ascii_value = stripped.encode("ascii", "ignore").decode("ascii")
    # Replace non-alphanumeric with dashes
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).lower()
    # Collapse multiple dashes and trim
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "missale-meum"


def _resolve_filename(title: str | None) -> str:
    if not title:
        return "missale-meum.pdf"
    slug = _slugify_for_filename(title)
    return f"{slug}.pdf"


__all__ = [
    "DEFAULT_LANGUAGE",
    "DEFAULT_VARIANT",
    "RenderedContent",
    "SITE_LABEL",
    "VARIANT_SPECS",
    "_apply_variant",
    "_get_translation_module",
    "_render_base_pdf",
    "_render_markdown",
    "_resolve_filename",
    "_slugify_for_filename",
    "_wrap_html",
    "cache",
]
