import datetime
import logging
import os
import sys
from enum import Enum
from typing import Any

import yaml
from fastapi import APIRouter, Depends, HTTPException, Path, status
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
)
from schemas import CalendarItem, ContentItem, Info, Proper


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


router = APIRouter()


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
        "Get the proper for a given observance by ID. The ID can be either a date in "
        "the `YYYY-MM-DD` format (e.g., `2025-11-11`), or a votive ID obtained from the "
        "`/votive` endpoint (e.g., `cordis-mariae`)."
    ),
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": PROPER_EXAMPLE
                }
            }
        }
    },
)
def v5_proper(
    date_or_id: str = Path(
        ..., description="ID of the proper.", example="cordis-mariae"
    ),
    lang: str = Depends(validate_locale),
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
    description="Get the Ordinary of the Mass — the invariable texts",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": ORDO_EXAMPLE
                }
            }
        }
    },
)
def v5_ordo(lang: str = Depends(validate_locale)) -> list[ContentItem]:
    with open(os.path.join(ORDO_DIR, lang, 'ordo.yaml')) as fh:
        raw_content = yaml.full_load(fh) or []
        if isinstance(raw_content, dict):
            raw_content = [raw_content]
        return [ContentItem.model_validate(item) for item in raw_content]


def supplement_response(
    lang: str,
    id_: str,
    subdir: SupplementCategory | None,
) -> list[ContentItem]:
    try:
        directory = subdir.value if isinstance(subdir, SupplementCategory) else subdir
        supplement_yaml = get_supplement(lang, id_, directory)
    except SupplementNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    else:
        content = ContentItem.model_validate(supplement_yaml)
        return [content]


@router.get(
    '/{lang}/api/v5/supplement/{id_}',
    response_model=list[ContentItem],
    summary="Get supplement content - default",
    description="Get supplement content from the default directory.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": SUPPLEMENT_CONTENT_EXAMPLE
                }
            }
        }
    },
)
def v5_supplement(
    id_: str = Path(..., description="ID of the resource.", example="info"),
    lang: str = Depends(validate_locale),
) -> list[ContentItem]:
    return supplement_response(lang, id_, None)


@router.get(
    '/{lang}/api/v5/supplement/{subdir}/{id_}',
    response_model=list[ContentItem],
    summary="Get supplement content",
    description="Get a specific supplement resource from a chosen subdirectory.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": SUPPLEMENT_CONTENT_EXAMPLE
                }
            }
        }
    },
)
def v5_supplement_resource(
    subdir: str = Path(
        ..., description="Type of supplement resource.", example="canticum"
    ),
    id_: str = Path(..., description="ID of the resource.", example="regina-caeli"),
    lang: str = Depends(validate_locale),
) -> list[ContentItem]:
    return supplement_response(lang, id_, subdir)


def _build_calendar(lang: str, year: int) -> list[CalendarItem]:
    missal: Calendar = controller.get_calendar(year, lang)
    container = []
    for date_, day in missal.items():
        title = day.get_celebration_name()
        tempora = day.get_tempora_name()
        tags: list[str] = []
        if tempora and title != tempora:
            tags.append(tempora)
        container.append({
            "title": title,
            "tags": tags,
            "colors": day.get_celebration_colors(),
            "rank": day.get_celebration_rank(),
            "id": date_.strftime("%Y-%m-%d"),
            "commemorations": day.get_commemorations_titles()
        })
    return [CalendarItem.model_validate(item) for item in container]


@router.get(
    '/{lang}/api/v5/calendar',
    response_model=list[CalendarItem],
    summary="Get current calendar",
    description="Get liturgical calendar according to the 1962 missal for the current year.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": CALENDAR_ITEMS_EXAMPLE
                }
            }
        }
    },
)
def v5_calendar_current(lang: str = Depends(validate_locale)) -> list[CalendarItem]:
    year = datetime.datetime.now().date().year
    return _build_calendar(lang, year)


@router.get(
    '/{lang}/api/v5/calendar/{year}',
    response_model=list[CalendarItem],
    summary="Get calendar for a given year",
    description="Get liturgical calendar according to the 1962 missal for the selected year.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": CALENDAR_ITEMS_EXAMPLE
                }
            }
        }
    },
)
def v5_calendar(
    year: int = Path(
        ...,
        description="Year of the calendar.",
        example=2022,
    ),
    lang: str = Depends(validate_locale),
) -> list[CalendarItem]:
    return _build_calendar(lang, year)


@router.get(
    '/{lang}/api/v5/votive',
    response_model=list[Info],
    summary="List votive Masses",
    description="Get the index of available votive Masses.",
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
    summary="List prayers",
    description="Get the index of available prayers",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": SUPPLEMENT_LIST_EXAMPLE
                }
            }
        }
    },
)
def v5_oratio(lang: str = Depends(validate_locale)) -> list[Info]:
    return [Info.model_validate(item) for item in supplement_index.get_oratio_index(lang)]


@router.get(
    '/{lang}/api/v5/oratio/{id_}',
    response_model=list[ContentItem],
    summary="Get prayer",
    description="Get specific prayer's content. This endpoint is a shortcut to `/{lang}/api/v5/supplement/{subdir}/{resource}` and can be used instead.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": SUPPLEMENT_CONTENT_EXAMPLE
                }
            }
        }
    },
)
def v5_oratio_by_id(
    id_: str = Path(..., description="ID of the resource.", example="aniele-bozy"),
    lang: str = Depends(validate_locale),
) -> list[ContentItem]:
    return supplement_response(lang, id_, SupplementCategory.ORATIO)


@router.get(
    '/{lang}/api/v5/canticum',
    response_model=list[Info],
    summary="Get chants",
    description="Get the index of available chants",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": SUPPLEMENT_LIST_EXAMPLE
                }
            }
        }
    },
)
def v5_canticum(lang: str = Depends(validate_locale)) -> list[Info]:
    return [Info.model_validate(item) for item in supplement_index.get_canticum_index(lang)]


@router.get(
    '/{lang}/api/v5/canticum/{id_}',
    response_model=list[ContentItem],
    summary="Get chant",
    description="Get specific chants's content. This endpoint is a shortcut to `/{lang}/api/v5/supplement/{subdir}/{resource}` and can be used instead.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": SUPPLEMENT_CONTENT_EXAMPLE
                }
            }
        }
    },
)
def v5_canticum_by_id(
    id_: str = Path(..., description="ID of the resource.", example="adoro-te"),
    lang: str = Depends(validate_locale),
) -> list[ContentItem]:
    return supplement_response(lang, id_, SupplementCategory.CANTICUM)


def _ical_response(lang: str, rank: int) -> PlainTextResponse:
    if rank not in range(1, 5):
        rank = 2

    content = controller.get_ical(lang, rank)
    return PlainTextResponse(content, media_type='text/calendar; charset=utf-8')


@router.get(
    '/{lang}/api/v5/icalendar',
    summary="Get calendar in iCalendar format",
    description=(
        "Get the calendar in iCalendar format, which can be imported to any calendar "
        "software such as Google Calendar. This endpoint returns only feast with rank 1 "
        "and 2. For other ranks see `/{lang}/api/v5/icalendar/{rank}`."
    ),
    responses={
        200: {
            "content": {
                "text/calendar": {
                    "example": ICALENDAR_EXAMPLE
                }
            }
        }
    },
)
def v5_ical(lang: str = Depends(validate_locale)) -> PlainTextResponse:
    return _ical_response(lang, rank=2)


@router.get(
    '/{lang}/api/v5/icalendar/{rank}',
    summary="Get calendar in iCalendar format",
    description=(
        "Get the calendar in iCalendar format, which can be imported to any calendar "
        "software such as Google Calendar."
    ),
    responses={
        200: {
            "content": {
                "text/calendar": {
                    "example": ICALENDAR_EXAMPLE
                }
            }
        }
    },
)
def v5_ical_for_rank(
    rank: int = Path(
        ...,
        description=(
            "Only show the feasts of this rank and higher (e.g. rank 2 will show feast "
            "with rank 1 and 2)."
        ),
        example=2,
    ),
    lang: str = Depends(validate_locale),
) -> PlainTextResponse:
    return _ical_response(lang, rank)


@router.get(
    '/{lang}/api/v5/version',
    summary="Get API version",
)
def v5_version(lang: str = Depends(validate_locale)) -> dict[str, str]:
    return {"version": __version__.__version__}


# Backwards compatibility for modules that still import `api`.
api = router
