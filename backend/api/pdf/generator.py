"""Generate printable PDFs for bilingual content.

This module mirrors the frontend printable view used by
``frontend/components/BilingualContent`` and the styles defined in
``frontend/components/styledComponents/printStyles.ts``. Instead of opening a
browser window, the backend now composes the same HTML structure and renders it
to PDF, allowing API clients to request ready-to-download documents.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from html import escape
from io import BytesIO
from types import ModuleType
from typing import Any
from unicodedata import normalize as _normalize

import mistune
from fastapi.responses import Response
from pydantic import BaseModel, ValidationError
from pypdf import PageObject, PdfReader, PdfWriter, Transformation
from weasyprint import HTML

from api.constants import TRANSLATION
from api.schemas import ContentItem, Info, Proper, ProperInfo, Section

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
    "a5": VariantSpec(page_size="A5", font_scale=0.9),
    "a6": VariantSpec(page_size="A6", font_scale=0.8),
    "a4-2pages": VariantSpec(page_size="A5", font_scale=0.9, mode="two_up", sheet_size="A4"),
    "a4-booklet": VariantSpec(page_size="A5", font_scale=0.9, mode="booklet", sheet_size="A4"),
    "a5-2pages": VariantSpec(page_size="A6", font_scale=0.8, mode="two_up", sheet_size="A5"),
    "a5-booklet": VariantSpec(page_size="A6", font_scale=0.8, mode="booklet", sheet_size="A5"),
}
DEFAULT_VARIANT = VARIANT_SPECS["a4"]
DEFAULT_LANGUAGE = "en"
SITE_LABEL = "www.missalemeum.com"


_MARKDOWN = mistune.create_markdown(
    escape=False,
    plugins=("strikethrough", "table", "task_lists", "footnotes", "abbr"),
)


@dataclass
class PrintableContent:
    """A normalised representation of incoming content blocks."""

    title: str
    description: str | None
    sections: Sequence[Section]
    meta_tags: Sequence[str]
    lang: str = DEFAULT_LANGUAGE


PrintableSource = Proper | ContentItem


def _resolve_language(*candidates: Any) -> str:
    for candidate in candidates:
        if candidate is None:
            continue
        value = str(candidate).strip().lower()
        if not value:
            continue
        if value in TRANSLATION:
            return value
    return DEFAULT_LANGUAGE


def _get_translation_module(lang: str) -> tuple[ModuleType, str]:
    if lang in TRANSLATION:
        return TRANSLATION[lang], lang
    if DEFAULT_LANGUAGE in TRANSLATION:
        return TRANSLATION[DEFAULT_LANGUAGE], DEFAULT_LANGUAGE
    # Fallback to any available translation module
    fallback_lang, module = next(iter(TRANSLATION.items()))
    return module, fallback_lang


def generate_pdf(
    *,
    payload: Any,
    variant: str,
    format_hint: str,
    lang: str | None = None,
    index: int = 0,
) -> Response:
    """Render incoming bilingual content into a styled PDF document."""

    _ = format_hint  # reserved for future content negotiation tweaks
    contents = _normalise_payload(payload, lang=lang)
    spec = VARIANT_SPECS.get(variant.lower(), DEFAULT_VARIANT)

    document_lang = lang or DEFAULT_LANGUAGE
    selected_index = _clamp_index(index, len(contents))
    html_document = _render_html_document(
        contents=contents,
        page_size=spec.page_size,
        font_scale=spec.font_scale,
        lang=document_lang,
        index=selected_index,
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


def _normalise_payload(payload: Any, lang: str | None = None) -> list[PrintableContent]:
    wrapped_items = _wrap_payload(payload)
    return [_build_content(item, lang) for item in wrapped_items]


def _clamp_index(index: int, length: int) -> int:
    if length <= 0:
        return 0
    try:
        value = int(index)
    except (TypeError, ValueError):
        value = 0
    upper_bound = min(length - 1, 2)
    if value < 0 or value > upper_bound:
        value = 0
    return value


def _wrap_payload(payload: Any) -> list[PrintableSource]:
    if payload is None:
        return []

    if isinstance(payload, (str, bytes)):
        return []

    candidates: list[Any]
    if isinstance(payload, (Proper, ContentItem)):
        candidates = [payload]
    elif isinstance(payload, BaseModel):
        candidates = [payload]
    elif isinstance(payload, Mapping):
        candidates = [payload]
    elif isinstance(payload, Iterable):
        candidates = list(payload)
    else:
        candidates = [payload]

    wrapped: list[PrintableSource] = []
    for candidate in candidates:
        parsed = _parse_payload_item(candidate)
        if parsed is not None:
            wrapped.append(parsed)
    return wrapped


def _parse_payload_item(candidate: Any) -> PrintableSource | None:
    if candidate is None:
        return None

    if isinstance(candidate, (Proper, ContentItem)):
        return candidate

    if isinstance(candidate, BaseModel):
        if isinstance(candidate, (Proper, ContentItem)):
            return candidate
        candidate = candidate.model_dump(mode="python")

    if isinstance(candidate, Mapping):
        for schema in (Proper, ContentItem):
            try:
                return schema.model_validate(candidate)
            except ValidationError:
                continue

    return None


def _build_content(item: PrintableSource, lang: str | None) -> PrintableContent:
    info = item.info
    title = str(info.title or "").strip() or "Missale Meum"
    description = getattr(info, "description", None)
    sections = item.sections or []
    content_lang = _resolve_language(lang)
    translation, resolved_lang = _get_translation_module(content_lang)
    meta_tags = _collect_meta_tags(info, translation)
    return PrintableContent(
        title=title,
        description=description,
        sections=sections,
        meta_tags=meta_tags,
        lang=resolved_lang,
    )


def _collect_meta_tags(info: Info | ProperInfo, translation: ModuleType) -> list[str]:
    tags: list[str] = []

    date_value = getattr(info, "date", None)
    if isinstance(date_value, str):
        tags.append(_format_date_label(date_value, translation))

    labels = getattr(translation, "PDF_LABELS", {})
    if not isinstance(labels, dict):
        labels = {}
    rank_label = labels.get("rank", "Rank")
    rank_value = getattr(info, "rank", None)
    if rank_value is not None:
        mapped_rank = None
        rank_map = getattr(translation, "PDF_RANK_LABELS", {})
        if isinstance(rank_map, Mapping):
            mapped_rank = rank_map.get(rank_value)
            if mapped_rank is None:
                try:
                    mapped_rank = rank_map[int(rank_value)]
                except (TypeError, ValueError, KeyError):
                    mapped_rank = None
        if mapped_rank:
            tags.append(str(mapped_rank))
        else:
            tags.append(f"{rank_label} {rank_value}")

    colors = getattr(info, "colors", None)
    if isinstance(colors, Sequence) and not isinstance(colors, (str, bytes)):
        if colors:
            colors_label = labels.get("colors", "Colors")
            color_map = getattr(translation, "PDF_COLOR_LABELS", {})
            if not isinstance(color_map, Mapping):
                color_map = {}
            for raw_color in colors:
                display = color_map.get(raw_color)
                if display is None:
                    try:
                        display = color_map.get(str(raw_color).lower())
                    except AttributeError:
                        display = None
                if display is None:
                    display = f"{colors_label}: {raw_color}"
                tags.append(str(display))

    extra_tags = info.tags or []
    if isinstance(extra_tags, Sequence) and not isinstance(extra_tags, (str, bytes)):
        for raw in extra_tags:
            tag = str(raw)
            if all([tag, not tag.startswith("Szaty"), not tag.startswith("Pallotinum")]):
                tags.append(tag)

    return tags


def _format_date_label(value: str, translation: ModuleType) -> str:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return value
    format_pattern = getattr(translation, "PDF_DATE_FORMAT", "{weekday}, {day} {month} {year}")
    months = getattr(translation, "PDF_DATE_MONTHS", ())
    weekdays = getattr(translation, "PDF_DATE_WEEKDAYS", ())

    if isinstance(months, Sequence) and len(months) > parsed.month:
        month_label = months[parsed.month]
    else:
        month_label = parsed.strftime("%B")

    weekday_index = parsed.weekday()
    if isinstance(weekdays, Sequence) and len(weekdays) > weekday_index:
        weekday_label = weekdays[weekday_index]
    else:
        weekday_label = parsed.strftime("%A")

    return format_pattern.format(day=parsed.day, month=month_label, year=parsed.year, weekday=weekday_label)


def _render_html_document(
    *,
    contents: Sequence[PrintableContent],
    page_size: str,
    font_scale: float,
    lang: str,
    index: int,
) -> str:
    if not contents:
        empty_body = """
        <div class=\"print-container\">
          <h1>Missale Meum</h1>
          <p class=\"print-paragraph\">No printable content was found for this request.</p>
        </div>
        """
        return _wrap_html(empty_body, page_size=page_size, font_scale=font_scale, title="Missale Meum", lang=lang)

    content = contents[index]
    body_html = _render_content_block(content)
    document_title = content.title
    return _wrap_html(body_html, page_size=page_size, font_scale=font_scale, title=document_title, lang=lang)


def _wrap_html(body_html: str, *, page_size: str, font_scale: float, title: str, lang: str) -> str:
    translation, resolved_lang = _get_translation_module(lang)
    labels = getattr(translation, "PDF_LABELS", {})
    if not isinstance(labels, dict):
        labels = {}
    page_label = labels.get("page", "Page")
    css = build_bilingual_print_styles(
        page_size=page_size,
        font_scale=font_scale,
        page_label=page_label,
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


def _render_content_block(content: PrintableContent) -> str:
    fragments: list[str] = ["<div class=\"print-container\">"]
    fragments.append(f"<h1>{escape(content.title)}</h1>")

    if content.meta_tags:
        meta_parts: list[str] = []
        for index, tag in enumerate(content.meta_tags):
            if index > 0:
                meta_parts.append('<span class="print-meta-separator">|</span>')
            meta_parts.append(f'<span>{escape(tag)}</span>')
        fragments.append(f'<div class="print-meta">{"".join(meta_parts)}</div>')

    if content.description:
        fragments.append(
            '<div class="print-paragraph">'
            f"{_render_markdown(content.description)}"
            "</div>"
        )

    for section in content.sections:
        fragments.append('<section class="print-section">')
        label = section.label
        if label:
            fragments.append(f"<h2>{escape(str(label))}</h2>")
        bodies = section.body
        if isinstance(bodies, Sequence):
            for paragraph in bodies:
                fragments.append(_render_paragraph(paragraph))
        fragments.append("</section>")

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
        f'<div class="print-column">{left}</div>'
        f'<div class="print-column">{right}</div>'
        '</div>'
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
    width_mm, height_mm = PAGE_DIMENSIONS_MM.get(size.upper(), PAGE_DIMENSIONS_MM[size])
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
