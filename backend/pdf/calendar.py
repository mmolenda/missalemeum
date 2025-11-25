"""Calendar-style PDF rendering."""
from __future__ import annotations

import calendar as _calendar
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime
from html import escape
from typing import Any

from pydantic import BaseModel, ValidationError

from api.constants import TRANSLATION
from api.schemas import CalendarItem

from .common import DEFAULT_LANGUAGE, _get_translation_module, _resolve_filename, _wrap_html


@dataclass
class NormalisedCalendarItem:
    identifier: str
    title: str
    date: date | None
    rank: int | None
    colors: list[str]
    commemorations: list[str]

FALLBACK_HEADING = "Other / Inne"


def _normalise_rank(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _normalise_strings(value: Any) -> list[str]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        result: list[str] = []
        for element in value:
            text = str(element or "").strip()
            if text:
                result.append(text)
        return result
    return []


def _normalise_calendar_payload(payload: Any) -> list[NormalisedCalendarItem]:
    raw_items = _extract_candidates(payload)
    normalised: list[NormalisedCalendarItem] = []
    for item in raw_items:
        identifier = str(item.id or "").strip()
        title = str(item.title or "").strip()
        if identifier and title:
            normalised.append(
                NormalisedCalendarItem(
                    identifier=identifier,
                    title=title,
                    date=_parse_calendar_date(identifier),
                    rank=_normalise_rank(getattr(item, "rank", None)),
                    colors=_normalise_strings(getattr(item, "colors", [])),
                    commemorations=_normalise_strings(
                        getattr(item, "commemorations", [])
                    ),
                )
            )
    return normalised


def _parse_calendar_date(identifier: str) -> date | None:
    try:
        return datetime.fromisoformat(identifier[:10]).date()
    except ValueError:
        return None


def _extract_candidates(payload: Any) -> list[CalendarItem]:
    if payload is None:
        return []

    if isinstance(payload, (str, bytes)):
        return []

    if isinstance(payload, CalendarItem):
        return [payload]

    if isinstance(payload, BaseModel):
        try:
            calendar_item = CalendarItem.model_validate(
                payload.model_dump(mode="python")
            )
        except ValidationError:
            return []
        return [calendar_item]

    if isinstance(payload, Mapping):
        try:
            return [CalendarItem.model_validate(payload)]
        except ValidationError:
            return []

    if isinstance(payload, Iterable):
        items: list[CalendarItem] = []
        for element in payload:
            if isinstance(element, CalendarItem):
                items.append(element)
                continue
            if isinstance(element, BaseModel):
                try:
                    element = element.model_dump(mode="python")
                except AttributeError:
                    continue
            if isinstance(element, Mapping):
                try:
                    items.append(CalendarItem.model_validate(element))
                except ValidationError:
                    continue
        return items

    return []


def is_calendar_payload(payload: Any) -> bool:
    return bool(_normalise_calendar_payload(payload))


def _resolve_month_label(month_index: int, lang: str) -> str:
    translation = TRANSLATION.get(lang)
    if translation is not None:
        months = getattr(translation, "MONTHS_NOMINATIVE", None)
        if isinstance(months, Sequence) and 0 < month_index < len(months):
            candidate = months[month_index]
            if candidate:
                return str(candidate)

    month_names = _calendar.month_name
    if 0 < month_index < len(month_names):
        return month_names[month_index]
    return str(month_index)


def _calendar_sort_key(item: NormalisedCalendarItem) -> tuple[object, ...]:
    date_value = item.date or date.max
    return (item.date is None, date_value, item.identifier)


def _group_by_year_and_month(
    items: Sequence[NormalisedCalendarItem],
) -> list[tuple[int | None, list[tuple[int | None, list[NormalisedCalendarItem]]]]]:
    grouped: list[
        tuple[int | None, list[tuple[int | None, list[NormalisedCalendarItem]]]]
    ] = []
    for item in items:
        year = item.date.year if item.date else None
        month = item.date.month if item.date else None
        if not grouped or grouped[-1][0] != year:
            grouped.append((year, []))
        months = grouped[-1][1]
        if not months or months[-1][0] != month:
            months.append((month, []))
        months[-1][1].append(item)
    return grouped


def _format_year_heading(year_value: int | None) -> str:
    if year_value is None:
        return FALLBACK_HEADING
    return str(year_value)


def _format_month_heading(month_index: int | None, *, lang: str) -> str:
    if month_index is None:
        return FALLBACK_HEADING
    return _resolve_month_label(month_index, lang)


def _format_weekday_label(value: date | None, translation: Any) -> str | None:
    if value is None:
        return None
    weekdays = getattr(translation, "PDF_DATE_WEEKDAYS", ())
    weekday_index = value.weekday()
    if isinstance(weekdays, Sequence) and 0 <= weekday_index < len(weekdays):
        weekday_label = weekdays[weekday_index]
        if weekday_label:
            return str(weekday_label)
    return value.strftime("%A")


def _format_rank_label(rank_value: int | None, translation: Any) -> str | None:
    if rank_value is None:
        return None

    labels = getattr(translation, "PDF_LABELS", {})
    rank_label = "Rank"
    if isinstance(labels, Mapping):
        rank_label = labels.get("rank", rank_label)

    rank_map = getattr(translation, "PDF_RANK_LABELS", {})
    mapped_rank = None
    if isinstance(rank_map, Mapping):
        mapped_rank = rank_map.get(rank_value)
        if mapped_rank is None:
            try:
                mapped_rank = rank_map.get(int(rank_value))
            except (TypeError, ValueError):
                mapped_rank = None
    if mapped_rank:
        return str(mapped_rank)
    return f"{rank_label} {rank_value}"


def _format_colors_label(colors: Sequence[str], translation: Any) -> str | None:
    if not colors:
        return None

    labels = getattr(translation, "PDF_LABELS", {})
    colors_label = "Colors"
    if isinstance(labels, Mapping):
        colors_label = labels.get("colors", colors_label)

    color_map = getattr(translation, "PDF_COLOR_LABELS", {})
    formatted: list[str] = []
    for raw_color in colors:
        display = None
        if isinstance(color_map, Mapping):
            display = color_map.get(raw_color)
            if display is None:
                try:
                    display = color_map.get(str(raw_color).lower())
                except AttributeError:
                    display = None
        formatted.append(str(display or f"{colors_label}: {raw_color}"))
    return ", ".join(formatted)


def _render_calendar_day(
    item: NormalisedCalendarItem,
    *,
    translation: Any,
) -> str:
    day_label = f"{item.date.day}." if item.date else "-"
    weekday_label = _format_weekday_label(item.date, translation)
    rank_label = _format_rank_label(item.rank, translation)
    colors_label = _format_colors_label(item.colors, translation)

    detail_segments: list[str] = []
    if weekday_label:
        detail_segments.append(
            f"<span class=\"calendar-day-weekday\">{escape(weekday_label)}</span>"
        )
    title_classes = ["calendar-day-title"]
    if item.rank in (1, 2):
        title_classes.append("calendar-day-title-strong")
    if item.rank == 1:
        title_classes.append("calendar-day-title-upper")
    detail_segments.append(
        f"<span class=\"{' '.join(title_classes)}\">{escape(item.title)}</span>"
    )
    if rank_label:
        detail_segments.append(
            f"<span class=\"calendar-day-rank\">{escape(rank_label)}</span>"
        )
    if colors_label:
        detail_segments.append(
            f"<span class=\"calendar-day-colors\">{escape(colors_label)}</span>"
        )

    separator = '<span class="calendar-separator">&ndash;</span>'
    details = f" {separator} ".join(detail_segments)

    commem_lines = [
        escape(commemoration)
        for commemoration in item.commemorations
        if commemoration
    ]
    commemorations_html = ""
    if commem_lines:
        commemorations_html = (
            '<div class="calendar-commemorations">'
            + "<br/>".join(commem_lines)
            + "</div>"
        )

    return (
        "<li class=\"calendar-day\">"
        "<div class=\"calendar-day-line\">"
        f"<span class=\"calendar-day-number\">{escape(day_label)}</span>"
        f"<span class=\"calendar-day-details\">{details}</span>"
        "</div>"
        f"{commemorations_html}"
        "</li>"
    )


def _build_cover_section(translation: Any, year_value: int | None) -> str:
    year_label = str(year_value) if year_value is not None else ""

    default_lines = [
        "MISSAL RUBRICAL GUIDE",
        "FOR THE POLISH DIOCESES",
        "FOR THE YEAR OF OUR LORD",
        "{year}",
        "ACCORDING TO THE 1962 ROMAN MISSAL",
    ]
    default_paragraphs = [
        (
            "This rubrical guide applies only to Masses celebrated in the "
            "Roman Rite prior to the 1970 reform."
        ),
        (
            "This guide has not been approved by the competent ecclesiastical "
            "authority. Therefore, in case of any error, the rubrics must be observed."
        ),
    ]
    default_footer = "Prepared by: missalemeum.com"

    lines = getattr(translation, "CALENDAR_COVER_LINES", None)
    paragraphs = getattr(translation, "CALENDAR_COVER_PARAGRAPHS", None)
    footer = getattr(translation, "CALENDAR_COVER_FOOTER", None)

    def _normalise_lines(
        value: Any, *, default: Sequence[str]
    ) -> list[str]:
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            result = [str(item).format(year=year_label) for item in value if str(item).strip()]
            if result:
                return result
        return [entry.format(year=year_label) for entry in default]

    cover_lines = _normalise_lines(lines, default=default_lines)
    cover_paragraphs = _normalise_lines(paragraphs, default=default_paragraphs)
    cover_footer = str(footer).strip() if isinstance(footer, str) else default_footer

    headline_fragments: list[str] = []
    for index, line in enumerate(cover_lines):
        if not line:
            continue
        classes = ["calendar-cover-line", "calendar-cover-headline"]
        if index == len(cover_lines) - 1:
            classes.append("calendar-cover-subheadline")
        headline_fragments.append(
            f'<div class=\"{" ".join(classes)}\">{escape(line)}</div>'
        )
    headline_html = "".join(headline_fragments)
    paragraph_html = "".join(
        f'<p class="calendar-cover-text">{escape(paragraph)}</p>'
        for paragraph in cover_paragraphs
    )
    footer_html = f'<div class="calendar-cover-footer">{escape(cover_footer)}</div>'

    return (
        '<section class="calendar-cover">'
        '<div class="calendar-cover-inner">'
        f"{headline_html}"
        '<div class="calendar-cover-body">'
        f"{paragraph_html}"
        f"{footer_html}"
        "</div>"
        "</div>"
        "</section>"
    )


def build_calendar_html(
    payload: Any,
    *,
    page_size: str,
    font_scale: float,
    lang: str | None,
) -> tuple[str, str]:
    items = _normalise_calendar_payload(payload)
    requested_lang = lang or DEFAULT_LANGUAGE
    translation, resolved_lang = _get_translation_module(requested_lang)
    if not items:
        body = """
        <div class="print-container">
          <h1>Missale Meum Calendar</h1>
          <p class="print-paragraph">No calendar entries were found for this request.</p>
        </div>
        """
        html_document = _wrap_html(
            body,
            page_size=page_size,
            font_scale=font_scale,
            title="Missale Meum Calendar",
            lang=resolved_lang,
        )
        return html_document, _resolve_filename("calendar")

    items = sorted(items, key=_calendar_sort_key)
    grouped_by_year = _group_by_year_and_month(items)
    first_year = next((year for year, _ in grouped_by_year if year is not None), None)

    cover_section = _build_cover_section(translation, first_year)
    year_sections: list[str] = []
    for year_value, months in grouped_by_year:
        month_sections: list[str] = []
        for month_index, month_items in months:
            heading = _format_month_heading(month_index, lang=resolved_lang)
            list_items = "".join(
                _render_calendar_day(month_item, translation=translation)
                for month_item in month_items
            )
            month_sections.append(
                "<section class=\"calendar-month\">"
                f"<h2 class=\"calendar-month-heading\">{escape(heading)}</h2>"
                f"<ol class=\"calendar-day-list\">{list_items}</ol>"
                "</section>"
            )
        year_sections.append(
            "<section class=\"calendar-year\">"
            f"{''.join(month_sections)}"
            "</section>"
        )

    document_title = "Missale Meum Calendar"
    if grouped_by_year:
        document_title = f"{_format_year_heading(grouped_by_year[0][0])} Calendar"

    body = (
        '<div class="print-container">'
        f"{cover_section}"
        f"{''.join(year_sections)}"
        "</div>"
    )
    html_document = _wrap_html(
        body,
        page_size=page_size,
        font_scale=font_scale,
        title=document_title,
        lang=resolved_lang,
    )
    first_identifier = items[0].identifier
    filename = _resolve_filename(f"calendar-{first_identifier}")
    return html_document, filename


__all__ = [
    "build_calendar_html",
    "is_calendar_payload",
]
