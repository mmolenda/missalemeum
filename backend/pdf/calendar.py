"""Calendar-style PDF rendering."""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from html import escape
from typing import Any

from pydantic import BaseModel, ValidationError

from api.schemas import CalendarItem

from .common import DEFAULT_LANGUAGE, _resolve_filename, _wrap_html


@dataclass
class NormalisedCalendarItem:
    identifier: str
    title: str


def _normalise_calendar_payload(payload: Any) -> list[NormalisedCalendarItem]:
    raw_items = _extract_candidates(payload)
    normalised: list[NormalisedCalendarItem] = []
    for item in raw_items:
        identifier = str(item.id or "").strip()
        title = str(item.title or "").strip()
        if identifier and title:
            normalised.append(NormalisedCalendarItem(identifier=identifier, title=title))
    return normalised


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

    list_items = "".join(
        f"<li><span class=\"calendar-id\">{escape(item.identifier)}</span> "
        f"<span class=\"calendar-title\">{escape(item.title)}</span></li>"
        for item in items
    )
    body = (
        '<div class="print-container">'
        "<h1>Missale Meum Calendar</h1>"
        f"<ul class=\"calendar-list\">{list_items}</ul>"
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
