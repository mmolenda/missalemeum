"""Generate printable PDFs for API responses."""
from __future__ import annotations

from typing import Any

from .calendar import build_calendar_html, is_calendar_payload
from .common import (
    DEFAULT_LANGUAGE,
    DEFAULT_VARIANT,
    RenderedContent,
    VARIANT_SPECS,
    _apply_variant,
    _render_base_pdf,
    _render_markdown,
    _resolve_filename,
    _wrap_html,
    cache,
)
from .documents import (
    PrintableContent,
    _build_content,
    _clamp_index,
    _collect_meta_tags,
    _format_date_label,
    _inject_custom_label,
    _normalise_payload,
    _parse_payload_item,
    _render_content_block,
    _render_html_document,
    _render_paragraph,
    _resolve_language,
    _sanitize_custom_label,
    _should_append_przeorat_block,
    _wrap_payload,
)


def generate_pdf(
    *,
    payload: Any,
    variant: str,
    format_hint: str,
    request_path: str,
    lang: str | None = None,
    index: int = 0,
    custom_label: str | None = None,
) -> RenderedContent:
    """Render incoming content into a styled PDF document."""
    cache_key = f"{request_path}/{index}/{format_hint}/{variant}/{custom_label}"
    if cache_key in cache:
        rendered_content: RenderedContent = cache[cache_key]
        return RenderedContent(
            filename=rendered_content.filename,
            pdf_bytes=rendered_content.pdf_bytes,
        )

    spec = VARIANT_SPECS.get(variant.lower(), DEFAULT_VARIANT)
    document_lang = lang or DEFAULT_LANGUAGE

    if is_calendar_payload(payload):
        html_document, filename = build_calendar_html(
            payload,
            page_size=spec.page_size,
            font_scale=spec.font_scale,
            lang=document_lang,
        )
    else:
        contents = _normalise_payload(payload, lang=lang)
        sanitized_label = _sanitize_custom_label(custom_label)
        if sanitized_label:
            contents = _inject_custom_label(contents, sanitized_label)
        selected_index = _clamp_index(index, len(contents))
        html_document = _render_html_document(
            contents=contents,
            page_size=spec.page_size,
            font_scale=spec.font_scale,
            lang=document_lang,
            index=selected_index,
            is_booklet=spec.mode == "booklet",
        )
        first_title = contents[0].title if contents else None
        filename = _resolve_filename(first_title)

    base_pdf_bytes = _render_base_pdf(html_document)
    pdf_bytes = _apply_variant(base_pdf_bytes, spec)

    rendered_content = RenderedContent(filename=filename, pdf_bytes=pdf_bytes)
    cache.set(cache_key, rendered_content, expire=None)
    return rendered_content


__all__ = [
    "PrintableContent",
    "DEFAULT_VARIANT",
    "RenderedContent",
    "VARIANT_SPECS",
    "generate_pdf",
    "_apply_variant",
    "_build_content",
    "_clamp_index",
    "_collect_meta_tags",
    "_format_date_label",
    "_inject_custom_label",
    "_normalise_payload",
    "_parse_payload_item",
    "_render_base_pdf",
    "_render_content_block",
    "_render_html_document",
    "_render_markdown",
    "_render_paragraph",
    "_resolve_filename",
    "_resolve_language",
    "_sanitize_custom_label",
    "_should_append_przeorat_block",
    "_wrap_html",
    "_wrap_payload",
]
