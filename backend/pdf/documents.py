"""Document-style PDF rendering (propers, prayers, chants)."""
from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Any
import re
import unicodedata
from html import escape

from pydantic import BaseModel, ValidationError

from api.constants import TRANSLATION
from api.schemas import ContentItem, Info, Proper, ProperInfo, Section

from .common import DEFAULT_LANGUAGE, _get_translation_module, _render_markdown, _wrap_html


_CUSTOM_LABEL_PATTERN = re.compile(r"^[A-Za-z0-9ĄĆĘŁŃÓŚŹŻąćęłńóśźż.,\- ]+$")


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


def _collect_meta_tags(info: Info | ProperInfo, translation: Any) -> list[str]:
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


def _format_date_label(value: str, translation: Any) -> str:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return value
    format_pattern = getattr(
        translation, "PDF_DATE_FORMAT", "{weekday}, {day} {month} {year}"
    )
    months = getattr(translation, "MONTHS_GENITIVE", None)
    if not isinstance(months, Sequence):
        months = getattr(translation, "MONTHS_NOMINATIVE", ())
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
        <div class="print-container">
          <h1>Missale Meum</h1>
          <p class="print-paragraph">No printable content was found for this request.</p>
        </div>
        """
        return _wrap_html(
            empty_body,
            page_size=page_size,
            font_scale=font_scale,
            title="Missale Meum",
            lang=lang,
        )

    content = contents[index]
    body_html = _render_content_block(content, is_booklet=is_booklet)
    document_title = content.title
    return _wrap_html(
        body_html,
        page_size=page_size,
        font_scale=font_scale,
        title=document_title,
        lang=lang,
    )


def _render_content_block(content: PrintableContent, *, is_booklet: bool) -> str:
    fragments: list[str] = ['<div class="print-container">']
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

    if _should_append_przeorat_block(content, is_booklet=is_booklet):
        fragments.append(_build_przeorat_block_html())

    fragments.append("</div>")
    return "".join(fragments)


def _should_append_przeorat_block(content: PrintableContent, *, is_booklet: bool) -> bool:
    if not is_booklet:
        return False
    if str(content.lang).strip().lower() != "pl":
        return False
    for raw_tag in content.meta_tags:
        tag = str(raw_tag).strip().lower()
        if "przeorat" in tag and "gdynia" in tag:
            return True
    return False


def _build_przeorat_block_html() -> str:
    rows = ["żałuję", "postanawiam", "adoruję", "dziękuję", "proszę"]
    fragments = ['<div class="przeorat-block"><ul>']
    for row in rows:
        fragments.append(f"<li>{escape(row)}</li>")
    fragments.append("</ul></div>")
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


__all__ = [
    "PrintableContent",
    "_build_content",
    "_build_przeorat_block_html",
    "_clamp_index",
    "_collect_meta_tags",
    "_format_date_label",
    "_inject_custom_label",
    "_normalise_payload",
    "_parse_payload_item",
    "_render_content_block",
    "_render_html_document",
    "_render_paragraph",
    "_resolve_language",
    "_sanitize_custom_label",
    "_should_append_przeorat_block",
    "_wrap_payload",
]
