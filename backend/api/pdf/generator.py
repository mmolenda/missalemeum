"""Generate printable PDFs for bilingual content.

This module mirrors the frontend printable view used by
``frontend/components/BilingualContent`` and the styles defined in
``frontend/components/styledComponents/printStyles.ts``. Instead of opening a
browser window, the backend now composes the same HTML structure and renders it
to PDF, allowing API clients to request ready-to-download documents.
"""
from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime
from html import escape
from io import BytesIO
from typing import Any
from unicodedata import normalize as _normalize

import mistune
from fastapi.responses import Response
from pypdf import PageObject, PdfReader, PdfWriter, Transformation
from weasyprint import HTML

from .styles import build_bilingual_print_styles

MM_TO_PT = 72 / 25.4
PAGE_DIMENSIONS_MM: dict[str, tuple[float, float]] = {
    "A4": (210.0, 297.0),
    "A5": (148.0, 210.0),
    "A6": (105.0, 148.0),
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
    "a5": VariantSpec(page_size="A5", font_scale=0.8),
    "a6": VariantSpec(page_size="A6", font_scale=0.6),
    "a4-2pages": VariantSpec(page_size="A5", font_scale=0.8, mode="two_up", sheet_size="A4"),
    "a4-booklet": VariantSpec(page_size="A5", font_scale=0.8, mode="booklet", sheet_size="A4"),
}
DEFAULT_VARIANT = VARIANT_SPECS["a4"]


_MARKDOWN = mistune.create_markdown(
    escape=False,
    plugins=("strikethrough", "table", "task_lists", "footnotes", "abbr"),
)


@dataclass
class PrintableContent:
    """A normalised representation of incoming content blocks."""

    title: str
    description: str | None
    sections: Sequence[dict[str, Any]]
    meta_tags: Sequence[str]


def generate_pdf(*, payload: Any, variant: str, format_hint: str) -> Response:
    """Render incoming bilingual content into a styled PDF document."""

    _ = format_hint  # reserved for future content negotiation tweaks
    contents = _normalise_payload(payload)
    spec = VARIANT_SPECS.get(variant.lower(), DEFAULT_VARIANT)

    html_document = _render_html_document(
        contents=contents,
        page_size=spec.page_size,
        font_scale=spec.font_scale,
    )

    base_pdf_bytes = HTML(string=html_document).write_pdf()

    if spec.mode == "two_up":
        sheet_size = spec.sheet_size or "A4"
        pdf_bytes = _impose_two_up(base_pdf_bytes, sheet_size)
    elif spec.mode == "booklet":
        sheet_size = spec.sheet_size or "A4"
        pdf_bytes = _impose_booklet(base_pdf_bytes, sheet_size)
    else:
        pdf_bytes = base_pdf_bytes

    filename = _resolve_filename(contents)
    headers = {
        "Content-Disposition": f"attachment; filename=\"{filename}\"",
    }

    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)


def _normalise_payload(payload: Any) -> list[PrintableContent]:
    if payload is None:
        return []

    if isinstance(payload, dict) and "info" in payload and "sections" in payload:
        return [_build_content(payload)]

    if isinstance(payload, Iterable) and not isinstance(payload, (str, bytes)):
        contents: list[PrintableContent] = []
        for item in payload:
            if isinstance(item, dict) and "info" in item and "sections" in item:
                contents.append(_build_content(item))
        return contents

    return []


def _build_content(item: dict[str, Any]) -> PrintableContent:
    info = item.get("info", {}) or {}
    title = str(info.get("title", "")) or "Missale Meum"
    description = info.get("description")
    sections = item.get("sections") or []
    meta_tags = _collect_meta_tags(info)
    return PrintableContent(title=title, description=description, sections=sections, meta_tags=meta_tags)


def _collect_meta_tags(info: dict[str, Any]) -> list[str]:
    tags: list[str] = []

    date_value = info.get("date")
    if isinstance(date_value, str):
        tags.append(_format_date_label(date_value))

    if info.get("tempora"):
        tags.append(str(info["tempora"]))

    if info.get("rank") is not None:
        tags.append(f"Rank {info['rank']}")

    colors = info.get("colors")
    if isinstance(colors, Sequence) and not isinstance(colors, (str, bytes)):
        if colors:
            tags.append("Colors: " + ", ".join(str(c) for c in colors))

    extra_tags = info.get("tags")
    if isinstance(extra_tags, Sequence) and not isinstance(extra_tags, (str, bytes)):
        for raw in extra_tags:
            tag = str(raw)
            if tag:
                tags.append(tag)

    commemorations = info.get("commemorations")
    if isinstance(commemorations, Sequence) and not isinstance(commemorations, (str, bytes)):
        for commemor in commemorations:
            label = str(commemor)
            if label:
                tags.append(label)

    supplements = info.get("supplements")
    if isinstance(supplements, Sequence) and not isinstance(supplements, (str, bytes)):
        for supplement in supplements:
            label = (supplement or {}).get("label") if isinstance(supplement, dict) else None
            if label:
                tags.append(str(label))

    return tags


def _format_date_label(value: str) -> str:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return value
    return parsed.strftime("%d %B %Y (%A)")


def _render_html_document(*, contents: Sequence[PrintableContent], page_size: str, font_scale: float) -> str:
    if not contents:
        empty_body = """
        <div class=\"print-container\">
          <h1>Missale Meum</h1>
          <p class=\"print-paragraph\">No printable content was found for this request.</p>
        </div>
        """
        return _wrap_html(empty_body, page_size=page_size, font_scale=font_scale, title="Missale Meum")

    body_fragments: list[str] = []
    for index, content in enumerate(contents):
        body_fragments.append(_render_content_block(content))
        if index < len(contents) - 1:
            body_fragments.append('<div class="print-page-break"></div>')

    document_title = contents[0].title
    body_html = "".join(body_fragments)
    return _wrap_html(body_html, page_size=page_size, font_scale=font_scale, title=document_title)


def _wrap_html(body_html: str, *, page_size: str, font_scale: float, title: str) -> str:
    css = build_bilingual_print_styles(page_size_rule=f"size: {page_size};", font_scale=font_scale)
    return (
        "<!DOCTYPE html>"
        "<html lang=\"en\">"
        "<head>"
        "<meta charset=\"utf-8\"/>"
        f"<title>{escape(title)}</title>"
        f"<style>{css}</style>"
        "</head>"
        "<body class=\"print-body\">"
        f"{body_html}"
        "</body></html>"
    )


def _render_content_block(content: PrintableContent) -> str:
    fragments: list[str] = ["<div class=\"print-container\">"]
    fragments.append(f"<h1>{escape(content.title)}</h1>")

    if content.meta_tags:
        meta_html = "".join(f'<span class="print-tag">{escape(tag)}</span>' for tag in content.meta_tags)
        fragments.append(f'<div class="print-meta">{meta_html}</div>')

    if content.description:
        fragments.append(
            '<div class="print-paragraph">'
            f"{_render_markdown(content.description)}"
            "</div>"
        )

    for section in content.sections:
        fragments.append('<section class="print-section">')
        label = section.get("label") if isinstance(section, dict) else None
        if label:
            fragments.append(f"<h2>{escape(str(label))}</h2>")
        bodies = section.get("body") if isinstance(section, dict) else None
        if isinstance(bodies, Sequence):
            for paragraph in bodies:
                fragments.append(_render_paragraph(paragraph))
        fragments.append("</section>")

    fragments.append('<p class="print-footer"><em>https://www.missalemeum.com</em></p>')
    fragments.append("</div>")
    return "".join(fragments)


def _render_paragraph(paragraph: Any) -> str:
    if not isinstance(paragraph, Sequence) or isinstance(paragraph, (str, bytes)):
        return ""

    if len(paragraph) == 0:
        return ""

    if len(paragraph) == 1:
        return (
            '<div class="print-paragraph">'
            f"{_render_markdown(str(paragraph[0]))}"
            "</div>"
        )

    left = _render_markdown(str(paragraph[0]))
    right = _render_markdown(str(paragraph[1]))

    return (
        '<div class="print-dual-column">'
        '<div class="print-column"><div class="print-column-content">'
        f"{left}"
        "</div></div>"
        '<div class="print-column"><div class="print-column-content">'
        f"{right}"
        "</div></div></div>"
    )


def _render_markdown(text: str, *, markdown_newlines: bool | None = None) -> str:
    if markdown_newlines is None:
        markdown_newlines = False

    if not markdown_newlines:
        text = text.replace("\\\n", "\n")
        text = text.replace("\n", "  \n")

    return _MARKDOWN(text)


def _impose_two_up(base_pdf_bytes: bytes, sheet_size: str) -> bytes:
    reader = PdfReader(BytesIO(base_pdf_bytes))
    writer = PdfWriter()

    sheet_width, sheet_height = _page_dimensions(sheet_size, orientation="landscape")
    slot_width = sheet_width / 2

    pages = list(reader.pages)
    for index in range(0, len(pages), 2):
        dst = writer.add_blank_page(width=sheet_width, height=sheet_height)
        _merge_page_into_slot(dst, pages[index], slot_width, sheet_height, offset_x=0)
        if index + 1 < len(pages):
            _merge_page_into_slot(dst, pages[index + 1], slot_width, sheet_height, offset_x=slot_width)

    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def _impose_booklet(base_pdf_bytes: bytes, sheet_size: str) -> bytes:
    reader = PdfReader(BytesIO(base_pdf_bytes))
    pages = list(reader.pages)
    if not pages:
        return base_pdf_bytes

    writer = PdfWriter()
    sheet_width, sheet_height = _page_dimensions(sheet_size, orientation="landscape")
    slot_width = sheet_width / 2

    base_width = float(pages[0].mediabox.width)
    base_height = float(pages[0].mediabox.height)

    while len(pages) % 4 != 0:
        pages.append(PageObject.create_blank_page(width=base_width, height=base_height))

    left_index = len(pages) - 1
    right_index = 0

    while right_index < left_index:
        front_page = writer.add_blank_page(width=sheet_width, height=sheet_height)
        _merge_page_into_slot(front_page, pages[left_index], slot_width, sheet_height, offset_x=0)
        _merge_page_into_slot(front_page, pages[right_index], slot_width, sheet_height, offset_x=slot_width)
        right_index += 1
        left_index -= 1

        if right_index > left_index:
            break

        back_page = writer.add_blank_page(width=sheet_width, height=sheet_height)
        _merge_page_into_slot(back_page, pages[right_index], slot_width, sheet_height, offset_x=0)
        _merge_page_into_slot(back_page, pages[left_index], slot_width, sheet_height, offset_x=slot_width)
        right_index += 1
        left_index -= 1

    output = BytesIO()
    writer.write(output)
    return output.getvalue()


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


def _page_dimensions(size: str, *, orientation: str = "portrait") -> tuple[float, float]:
    width_mm, height_mm = PAGE_DIMENSIONS_MM.get(size.upper(), PAGE_DIMENSIONS_MM["A4"])
    if orientation == "landscape":
        width_mm, height_mm = height_mm, width_mm
    return width_mm * MM_TO_PT, height_mm * MM_TO_PT


def _resolve_filename(contents: Sequence[PrintableContent]) -> str:
    if not contents:
        return "missale-meum.pdf"

    title = contents[0].title or "missale-meum"
    slug = _slugify_for_filename(title)
    return f"{slug}.pdf"


def _slugify_for_filename(value: str) -> str:
    normalised = _normalize("NFKD", value)
    ascii_value = normalised.encode("ascii", "ignore").decode("ascii")
    cleaned = [char.lower() if char.isalnum() else "-" for char in ascii_value]
    slug = "".join(cleaned)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "missale-meum"
