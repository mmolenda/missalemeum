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

from .common import DEFAULT_LANGUAGE, _resolve_filename, _wrap_html


@dataclass
class NormalisedCalendarItem:
    identifier: str
    title: str
    date: date | None

FALLBACK_HEADING = "Other / Inne"


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
        months = getattr(translation, "PDF_DATE_MONTHS", ())
        if isinstance(months, Sequence) and 0 < month_index < len(months):
            candidate = months[month_index]
            if candidate:
                return str(candidate)

    month_names = _calendar.month_name
    if 0 < month_index < len(month_names):
        return month_names[month_index]
    return str(month_index)


def _format_month_heading(month_index: int | None) -> str:
    if month_index is None:
        return FALLBACK_HEADING
    english = _resolve_month_label(month_index, "en")
    polish = _resolve_month_label(month_index, "pl")
    return f"{english} / {polish}"


def build_calendar_html(
    payload: Any,
    *,
    page_size: str,
    font_scale: float,
    lang: str | None,
) -> tuple[str, str]:
    items = _normalise_calendar_payload(payload)
    lang_value = lang or DEFAULT_LANGUAGE
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
            lang=lang_value,
        )
        return html_document, _resolve_filename("calendar")

    items = sorted(items, key=lambda item: item.identifier)
    grouped: list[tuple[tuple[int, int] | None, list[NormalisedCalendarItem]]] = []
    for item in items:
        key: tuple[int, int] | None
        if item.date is None:
            key = None
        else:
            key = (item.date.year, item.date.month)
        if not grouped or grouped[-1][0] != key:
            grouped.append((key, []))
        grouped[-1][1].append(item)

    month_sections: list[str] = []
    for index, (group_key, month_items) in enumerate(grouped):
        classes = ["calendar-month-heading"]
        if index == 0:
            classes.append("calendar-month-heading-first")
        month_index = group_key[1] if group_key is not None else None
        heading = _format_month_heading(month_index)
        list_items = "".join(
            f"<li>{escape(item.title)}</li>"
            for item in month_items
        )
        month_sections.append(
            "<section class=\"calendar-month\">"
            f"<h2 class=\"{' '.join(classes)}\">{escape(heading)}</h2>"
            f"<ol class=\"calendar-list calendar-month-list\">{list_items}</ol>"
            "</section>"
        )

    body = (
        '<div class="print-container">'
        "<h1>Missale Meum Calendar</h1>"
        f"{''.join(month_sections)}"
        "</div>"
    )
    html_document = _wrap_html(
        body,
        page_size=page_size,
        font_scale=font_scale,
        title="Missale Meum Calendar",
        lang=lang_value,
    )
    first_identifier = items[0].identifier
    filename = _resolve_filename(f"calendar-{first_identifier}")
    return html_document, filename


__all__ = [
    "build_calendar_html",
    "is_calendar_payload",
]
