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
from typing import Any
from unicodedata import normalize as _normalize

import mistune
from fastapi.responses import Response
from weasyprint import HTML

from .styles import BILINGUAL_PRINT_STYLES

PAGE_SIZE_MAP: dict[str, str] = {
    "a4": "A4",
    "a5": "A5",
    "a6": "A6",
}

# NOTE: CSS rules live in :mod:`api.pdf.styles` so this module can focus on
# payload transformation and PDF rendering.

_MARKDOWN = mistune.create_markdown(
    escape=False,
    plugins=(
        "strikethrough",
        "table",
        "task_lists",
        "footnotes",
        "abbr",
    ),
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
    page_size = PAGE_SIZE_MAP.get(variant.lower(), PAGE_SIZE_MAP["a4"])
    html_document = _render_html_document(contents, page_size)
    pdf_bytes = HTML(string=html_document).write_pdf()

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


def _render_html_document(contents: Sequence[PrintableContent], page_size: str) -> str:
    if not contents:
        empty_body = """
        <div class=\"print-container\">
          <h1>Missale Meum</h1>
          <p class=\"print-paragraph\">No printable content was found for this request.</p>
        </div>
        """
        return _wrap_html(empty_body, page_size, title="Missale Meum")

    body_fragments: list[str] = []
    for index, content in enumerate(contents):
        body_fragments.append(_render_content_block(content))
        if index < len(contents) - 1:
            body_fragments.append('<div class="print-page-break"></div>')

    document_title = contents[0].title
    body_html = "".join(body_fragments)
    return _wrap_html(body_html, page_size, title=document_title)


def _wrap_html(body_html: str, page_size: str, *, title: str) -> str:
    css = BILINGUAL_PRINT_STYLES.format(page_size_rule=f"size: {page_size};")
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
