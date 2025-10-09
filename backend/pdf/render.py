"""Generate printable PDFs for bilingual content.

This module mirrors the frontend printable view used by
``frontend/components/BilingualContent`` and the styles defined in
``frontend/components/styledComponents/printStyles.ts``. Instead of opening a
browser window, the backend now composes the same HTML structure and renders it
to PDF, allowing API clients to request ready-to-download documents.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import datetime
from html import escape
from io import BytesIO
import logging
import os
import re
from types import ModuleType
from typing import Any
import unicodedata

import mistune
from pydantic import BaseModel, ValidationError
from pypdf import PageObject, PdfReader, PdfWriter, Transformation
from pypdf.generic import DecodedStreamObject, NameObject
from weasyprint import HTML

from api.constants import TRANSLATION
from api.schemas import ContentItem, Info, Proper, ProperInfo, Section

from .styles import build_bilingual_print_styles
from diskcache import Cache


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
}
DEFAULT_VARIANT = VARIANT_SPECS["a4"]
DEFAULT_LANGUAGE = "en"
SITE_LABEL = "www.missalemeum.com"

_CUSTOM_LABEL_PATTERN = re.compile(r"^[A-Za-z0-9ĄĆĘŁŃÓŚŹŻąćęłńóśźż.,\- ]+$")

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


@dataclass
class RenderedContent:
    filename: str
    pdf_bytes: bytes


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
    request_path: str,
    lang: str | None = None,
    index: int = 0,
    custom_label: str | None = None,
) -> RenderedContent:
    """Render incoming bilingual content into a styled PDF document."""
    cache_key = f"{request_path}/{index}/{format_hint}/{variant}/{custom_label}"
    if cache_key in cache:
        rendered_content: RenderedContent = cache[cache_key]
        return RenderedContent(filename=rendered_content.filename,
                               pdf_bytes=rendered_content.pdf_bytes)
    
    _ = format_hint  # reserved for future content negotiation tweaks
    contents = _normalise_payload(payload, lang=lang)
    sanitized_label = _sanitize_custom_label(custom_label)
    if sanitized_label:
        contents = _inject_custom_label(contents, sanitized_label)
    spec = VARIANT_SPECS.get(variant.lower(), DEFAULT_VARIANT)

    document_lang = lang or DEFAULT_LANGUAGE
    selected_index = _clamp_index(index, len(contents))
    html_document = _render_html_document(
        contents=contents,
        page_size=spec.page_size,
        font_scale=spec.font_scale,
        lang=document_lang,
        index=selected_index,
        is_booklet=spec.mode == "booklet",
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
    rendered_content = RenderedContent(filename=filename, pdf_bytes=pdf_bytes)
    cache.set(cache_key, rendered_content, expire=None)
    return rendered_content

def _normalise_payload(payload: Any, lang: str | None = None) -> list[PrintableContent]:
    wrapped_items = _wrap_payload(payload)
    return [_build_content(item, lang) for item in wrapped_items]


def _sanitize_custom_label(raw_label: str | None) -> str | None:
    if raw_label is None:
        return None

    candidate = unicodedata.normalize("NFKC", str(raw_label)).strip()
    if not candidate:
        return None
    if not 4 <= len(candidate) <= 64:
        return None
    if not _CUSTOM_LABEL_PATTERN.fullmatch(candidate):
        return None
    return candidate


def _inject_custom_label(contents: Sequence[PrintableContent], label: str) -> list[PrintableContent]:
    return [
        replace(content, meta_tags=[label, *list(content.meta_tags)])
        for content in contents
    ]


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
    is_booklet: bool,
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
    body_html = _render_content_block(content, is_booklet=is_booklet)
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


def _render_content_block(content: PrintableContent, *, is_booklet: bool) -> str:
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

    if _should_append_przeorat_table(content, is_booklet=is_booklet):
        fragments.append(_build_przeorat_table_html())

    fragments.append("</div>")
    return "".join(fragments)


def _should_append_przeorat_table(content: PrintableContent, *, is_booklet: bool) -> bool:
    if not is_booklet:
        return False
    if str(content.lang).strip().lower() != "pl":
        return False
    for raw_tag in content.meta_tags:
        tag = str(raw_tag).strip().lower()
        if "przeorat" in tag and "gdynia" in tag:
            return True
    return False


def _build_przeorat_table_html() -> str:
    rows = ["żałuję", "postanawiam", "adoruję", "dziękuję", "proszę"]
    fragments = ['<table class="przeorat-table"><tbody>']
    for row in rows:
        fragments.append("<tr>")
        fragments.append(f"<td>{escape(row)}</td>")
        fragments.append("<td></td>")
        fragments.append("</tr>")
    fragments.append("</tbody></table>")
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
        sheet = PageObject.create_blank_page(None, width=sheet_width, height=sheet_height)
        _merge_page_into_slot(sheet, pages[index], slot_width, sheet_height, offset_x=0)
        if index + 1 < len(pages):
            _merge_page_into_slot(sheet, pages[index + 1], slot_width, sheet_height, offset_x=slot_width)
        added_page = writer.add_page(sheet)
        added_page.compress_content_streams()

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
        "0.8 0.8 0.8 RG\n"
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


def _resolve_filename(contents: Sequence[PrintableContent]) -> str:
    if not contents:
        return "missale-meum.pdf"

    title = contents[0].title or "missale-meum"
    slug = _slugify_for_filename(title)
    return f"{slug}.pdf"


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
