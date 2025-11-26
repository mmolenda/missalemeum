import datetime
import logging
import os
import sys
from enum import Enum
from typing import Any

import yaml
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.responses import PlainTextResponse

import __version__
import controller
from api.exceptions import InvalidInput, ProperNotFound, SectionNotFound, SupplementNotFound
from constants import TRANSLATION
from constants.common import LANGUAGES, ORDO_DIR
from kalendar.models import Calendar, Day
from utils import format_propers, get_pregenerated_proper, get_supplement, supplement_index
from examples import (
    CALENDAR_ITEMS_EXAMPLE,
    ICALENDAR_EXAMPLE,
    ORDO_EXAMPLE,
    PROPER_EXAMPLE,
    SUPPLEMENT_CONTENT_EXAMPLE,
    SUPPLEMENT_LIST_EXAMPLE,
    VOTIVE_LIST_EXAMPLE,
    get_json_response,
    get_text_response,
)
from pdf import PDFAwareRoute, PdfOptions, get_pdf_options
from schemas import CalendarItem, ContentItem, Info, Proper, VersionInfo


class LanguageCode(str, Enum):
    EN = "en"
    PL = "pl"


class SupplementCategory(str, Enum):
    SUPPLEMENT = "supplement"
    ORATIO = "oratio"
    CANTICUM = "canticum"

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s ] %(levelname)s in %(module)s: %(message)s')


router = APIRouter(route_class=PDFAwareRoute)


def validate_locale(
    lang: LanguageCode = Path(..., description="Language of the response."),
) -> str:
    value = lang.value
    if value not in LANGUAGES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return value


def _parse_propers(payload: list[dict[str, Any]]) -> list[Proper]:
    return [Proper.model_validate(item) for item in payload]


@router.get(
    '/{lang}/api/v5/proper/{date_or_id}',
    response_model=list[Proper],
    summary="Get Proper by ID",
    description=(
        "Get the Proper for an observance by ID or date. The ID can be a date in "
        "`YYYY-MM-DD` format (e.g., `2025-11-11`) or a votive ID from the `/votive` "
        "endpoint (e.g., `cordis-mariae`)."
    ),
    responses=get_json_response(PROPER_EXAMPLE)
)
def v5_proper(
    date_or_id: str = Path(
        ...,
        description="ID of the proper.",
        json_schema_extra={
            "example": "2025-11-11"
        },
    ),
    lang: str = Depends(validate_locale),
    _pdf_options: PdfOptions = Depends(get_pdf_options),
) -> list[Proper]:
    try:
        date_object = datetime.datetime.strptime(date_or_id, "%Y-%m-%d").date()
    except ValueError:
        # Not a valid date, getting by ID
        proper_id = {i['ref']: i['id'] for i in TRANSLATION[lang].VOTIVE_MASSES}.get(date_or_id, date_or_id)
        try:
            pregenerated_proper = get_pregenerated_proper(lang, proper_id)
            if pregenerated_proper is not None:
                return _parse_propers(pregenerated_proper)
            proper_vernacular, proper_latin = controller.get_proper_by_id(proper_id, lang)
            return _parse_propers(format_propers([[proper_vernacular, proper_latin]]))
        except InvalidInput as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
        except ProperNotFound as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
        except SectionNotFound as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    else:
        # Valid date, getting day's proper
        day: Day = controller.get_day(date_object, lang)
        pregenerated_proper = get_pregenerated_proper(lang, day.get_celebration_id(), day.get_tempora_id())
        if pregenerated_proper:
            return _parse_propers(pregenerated_proper)
        return _parse_propers(format_propers(day.get_proper(), day))


@router.get(
    '/{lang}/api/v5/ordo',
    response_model=list[ContentItem],
    summary="Get Ordinary",
    description="Get the Ordinary of the Mass — the invariable texts.",
    responses=get_json_response(ORDO_EXAMPLE)
)
def v5_ordo(
    lang: str = Depends(validate_locale),
    _pdf_options: PdfOptions = Depends(get_pdf_options),
) -> list[ContentItem]:
    with open(os.path.join(ORDO_DIR, lang, 'ordo.yaml')) as fh:
        raw_content = yaml.full_load(fh) or []
        if isinstance(raw_content, dict):
            raw_content = [raw_content]
        return [ContentItem.model_validate(item) for item in raw_content]


def supplement_response(
    lang: str,
    id_: str,
    subdir: SupplementCategory | str | None,
) -> list[ContentItem]:
    directory = subdir.value if isinstance(subdir, SupplementCategory) else subdir
    try:
        supplement_yaml = get_supplement(lang, id_, directory)
    except SupplementNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    content = ContentItem.model_validate(supplement_yaml)
    return [content]


@router.get(
    '/{lang}/api/v5/supplement/{id_}',
    response_model=list[ContentItem],
    summary="Get Supplement Content (Default)",
    description="Get supplement content from the default directory.",
    responses=get_json_response(SUPPLEMENT_CONTENT_EXAMPLE),
)
def v5_supplement(
    id_: str = Path(
        ...,
        description="ID of the resource.",
        json_schema_extra={"example": "info"},
    ),
    lang: str = Depends(validate_locale),
    _pdf_options: PdfOptions = Depends(get_pdf_options),
) -> list[ContentItem]:
    return supplement_response(lang, id_, None)


def _build_calendar_response(lang: str, year: int, month: int | None = None) -> list[CalendarItem]:
    missal: Calendar = controller.get_calendar(year, lang)
    container = []
    for date_, day in missal.items():
        if month is not None and date_.month != month:
            continue
        container.append(_calendar_item_from_day(date_, day))
    return container


def _calendar_item_from_day(date_: datetime.date, day: Day) -> CalendarItem:
    title = day.get_celebration_name()
    tempora = day.get_tempora_name()
    tags: list[str] = []
    if tempora and title != tempora:
        tags.append(tempora)
    payload = {
        "title": title,
        "tags": tags,
        "colors": day.get_celebration_colors(),
        "rank": day.get_celebration_rank(),
        "id": date_.strftime("%Y-%m-%d"),
        "commemorations": day.get_commemorations_titles(),
    }
    return CalendarItem.model_validate(payload)


def _parse_query_date(value: str, field_name: str) -> datetime.date:
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        message = f"Invalid {field_name} date format. Use YYYY-MM-DD."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message) from exc


@router.get(
    '/{lang}/api/v5/calendar',
    response_model=list[CalendarItem],
    summary="Get Calendar (current)",
    description="Get the liturgical calendar for the current year.",
    responses=get_json_response(CALENDAR_ITEMS_EXAMPLE),
)
def v5_calendar_current(
    lang: str = Depends(validate_locale),
    _pdf_options: PdfOptions = Depends(get_pdf_options),
) -> list[CalendarItem]:
    target_year = datetime.datetime.now().date().year
    return _build_calendar_response(lang, target_year)


@router.get(
    '/{lang}/api/v5/calendar/range',
    response_model=list[CalendarItem],
    summary="Get Calendar (range)",
    description="Get the liturgical calendar between two dates (inclusive).",
    responses=get_json_response(CALENDAR_ITEMS_EXAMPLE),
)
def v5_calendar_range(
    from_: str = Query(
        ...,
        alias="from",
        description="Start date in YYYY-MM-DD format.",
        json_schema_extra={"example": "2025-01-01"},
    ),
    until: str = Query(
        ...,
        description="End date in YYYY-MM-DD format.",
        json_schema_extra={"example": "2025-03-01"},
    ),
    lang: str = Depends(validate_locale),
) -> list[CalendarItem]:
    start_date = _parse_query_date(from_, "from")
    end_date = _parse_query_date(until, "until")

    if start_date >= end_date:
        detail = "`from` must be earlier than `until`."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    if (end_date - start_date).days > 120:
        detail = "The range cannot exceed 120 days."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    years = {start_date.year, end_date.year}
    calendars = {year: controller.get_calendar(year, lang) for year in years}

    items: list[CalendarItem] = []
    current = start_date
    while current <= end_date:
        calendar = calendars[current.year]
        day = calendar.get_day(current)
        if day is None:
            detail = f"Calendar data not found for {current.isoformat()}."
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        items.append(_calendar_item_from_day(current, day))
        current += datetime.timedelta(days=1)

    return items


@router.get(
    '/{lang}/api/v5/calendar/{year}',
    response_model=list[CalendarItem],
    summary="Get Calendar (year)",
    description="Get the liturgical calendar for a given year.",
    responses=get_json_response(CALENDAR_ITEMS_EXAMPLE),
)
def v5_calendar_year(
    year: int = Path(
        ...,
        description="Year of the calendar.",
        json_schema_extra={"example": 2025},
    ),
    lang: str = Depends(validate_locale),
    _pdf_options: PdfOptions = Depends(get_pdf_options),
) -> list[CalendarItem]:
    return _build_calendar_response(lang, year)

@router.get(
    '/{lang}/api/v5/votive',
    response_model=list[Info],
    summary="List Votive Masses",
    description="List available votive Masses.",
    responses=get_json_response(VOTIVE_LIST_EXAMPLE),
)
def v5_votive(lang: str = Depends(validate_locale)) -> list[Info]:
    index = TRANSLATION[lang].VOTIVE_MASSES
    return [
        Info.model_validate({
            "id": i['ref'],
            "title": i['title'],
            "tags": i['tags'],
        })
        for i in index
    ]


@router.get(
    '/{lang}/api/v5/oratio',
    response_model=list[Info],
    summary="List Prayers",
    description="List available prayers.",
    responses=get_json_response(SUPPLEMENT_LIST_EXAMPLE),
)
def v5_oratio(lang: str = Depends(validate_locale)) -> list[Info]:
    return [Info.model_validate(item) for item in supplement_index.get_oratio_index(lang)]


@router.get(
    '/{lang}/api/v5/oratio/{id_}',
    response_model=list[ContentItem],
    summary="Get Prayer",
    description=(
        "Get a specific prayer’s content. This endpoint is a shortcut to "
        "`/{lang}/api/v5/supplement/{subdir}/{id_}`."
    ),
    responses=get_json_response(SUPPLEMENT_CONTENT_EXAMPLE),
)
def v5_oratio_by_id(
    id_: str = Path(
        ...,
        description="ID of the resource.",
        json_schema_extra={"example": "magnificat"},
    ),
    lang: str = Depends(validate_locale),
    _pdf_options: PdfOptions = Depends(get_pdf_options),
) -> list[ContentItem]:
    return supplement_response(lang, id_, SupplementCategory.ORATIO)


@router.get(
    '/{lang}/api/v5/canticum',
    response_model=list[Info],
    summary="List Chants",
    description="List available chants.",
    responses=get_json_response(SUPPLEMENT_LIST_EXAMPLE),
)
def v5_canticum(lang: str = Depends(validate_locale)) -> list[Info]:
    return [Info.model_validate(item) for item in supplement_index.get_canticum_index(lang)]


@router.get(
    '/{lang}/api/v5/canticum/{id_}',
    response_model=list[ContentItem],
    summary="Get Chant",
    description=(
        "Get a specific chant’s content. This endpoint is a shortcut to "
        "`/{lang}/api/v5/supplement/{subdir}/{id_}`."
    ),
    responses=get_json_response(SUPPLEMENT_CONTENT_EXAMPLE),
)
def v5_canticum_by_id(
    id_: str = Path(
        ...,
        description="ID of the resource.",
        json_schema_extra={"example": "salve-regina"},
    ),
    lang: str = Depends(validate_locale),
    _pdf_options: PdfOptions = Depends(get_pdf_options),
) -> list[ContentItem]:
    return supplement_response(lang, id_, SupplementCategory.CANTICUM)


def _ical_response(lang: str, rank: int | None = None) -> PlainTextResponse:
    target_rank = rank if rank is not None else 2
    if target_rank not in range(1, 5):
        target_rank = 2

    content = controller.get_ical(lang, target_rank)
    return PlainTextResponse(content, media_type='text/calendar; charset=utf-8')


@router.get(
    '/{lang}/api/v5/icalendar',
    summary="Get Calendar (iCalendar Format)",
    description=(
        "Get the calendar in iCalendar format, which can be imported into calendar "
        "software such as Google Calendar. By default, only feasts with ranks 1 and 2 "
        "are included; set `rank` to include lower ranks."
    ),
    responses=get_text_response(ICALENDAR_EXAMPLE, media_type='text/calendar'),
)
def v5_ical_current(lang: str = Depends(validate_locale)) -> PlainTextResponse:
    return _ical_response(lang)


@router.get(
    '/{lang}/api/v5/icalendar/{rank}',
    summary="Get Calendar (iCalendar Format)",
    description="Get the calendar in iCalendar format for a specific rank.",
    responses=get_text_response(ICALENDAR_EXAMPLE, media_type='text/calendar'),
)
def v5_ical(
    rank: int = Path(
        ...,
        ge=1,
        le=4,
        description="Only show the feasts of this rank and higher (1-4).",
        json_schema_extra={"example": 2},
    ),
    lang: str = Depends(validate_locale),
) -> PlainTextResponse:
    return _ical_response(lang, rank)


@router.get(
    '/{lang}/api/v5/version',
    response_model=VersionInfo,
    summary="Get API Version",
)
def v5_version(lang: str = Depends(validate_locale)) -> VersionInfo:
    return VersionInfo(version=__version__.__version__)


# Backwards compatibility for modules that still import `api`.
api = router
