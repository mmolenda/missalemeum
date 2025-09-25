import datetime
import logging
import os
import sys
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
from schemas import ContentItem

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s ] %(levelname)s in %(module)s: %(message)s')


router = APIRouter()


def validate_locale(lang: str = Path(...)) -> str:
    if lang not in LANGUAGES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return lang


@router.get('/{lang}/api/v5/proper/{date_or_id}')
def v5_proper(date_or_id: str, lang: str = Depends(validate_locale)) -> Any:
    try:
        date_object = datetime.datetime.strptime(date_or_id, "%Y-%m-%d").date()
    except ValueError:
        # Not a valid date, getting by ID
        proper_id = {i['ref']: i['id'] for i in TRANSLATION[lang].VOTIVE_MASSES}.get(date_or_id, date_or_id)
        try:
            pregenerated_proper = get_pregenerated_proper(lang, proper_id)
            if pregenerated_proper is not None:
                return pregenerated_proper
            proper_vernacular, proper_latin = controller.get_proper_by_id(proper_id, lang)
            return format_propers([[proper_vernacular, proper_latin]])
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
            return pregenerated_proper
        return format_propers(day.get_proper(), day)


@router.get('/{lang}/api/v5/ordo')
def v5_ordo(lang: str = Depends(validate_locale)) -> Any:
    with open(os.path.join(ORDO_DIR, lang, 'ordo.yaml')) as fh:
        content = yaml.full_load(fh)
        return content


def supplement_response(lang: str, id_: str, subdir: str | None) -> list[ContentItem]:
    try:
        supplement_yaml = get_supplement(lang, id_, subdir)
    except SupplementNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    else:
        content = ContentItem.model_validate(supplement_yaml)
        return [content]


@router.get('/{lang}/api/v5/supplement/{id_}', response_model=list[ContentItem])
def v5_supplement(
    id_: str,
    lang: str = Depends(validate_locale),
) -> list[ContentItem]:
    return supplement_response(lang, id_, None)


@router.get('/{lang}/api/v5/supplement/{subdir}/{resource}', response_model=list[ContentItem])
def v5_supplement_resource(
    subdir: str,
    resource: str,
    lang: str = Depends(validate_locale),
) -> list[ContentItem]:
    return supplement_response(lang, resource, subdir)


@router.get('/{lang}/api/v5/calendar')
@router.get('/{lang}/api/v5/calendar/{year}')
def v5_calendar(
    year: int | None = None,
    lang: str = Depends(validate_locale),
) -> list[dict[str, Any]]:
    if year is None:
        year = datetime.datetime.now().date().year
    missal: Calendar = controller.get_calendar(year, lang)
    container = []
    for date_, day in missal.items():
        title = day.get_celebration_name()
        tempora = day.get_tempora_name()
        tags = []
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
    return container


@router.get('/{lang}/api/v5/votive')
def v5_votive(lang: str = Depends(validate_locale)) -> list[dict[str, Any]]:
    index = TRANSLATION[lang].VOTIVE_MASSES
    return [{
        "id": i['ref'],
        "title": i["title"],
        "tags": i["tags"]
    } for i in index]


@router.get('/{lang}/api/v5/oratio')
def v5_oratio(lang: str = Depends(validate_locale)) -> Any:
    return supplement_index.get_oratio_index(lang)


@router.get('/{lang}/api/v5/oratio/{id_}', response_model=list[ContentItem])
def v5_oratio_by_id(id_: str, lang: str = Depends(validate_locale)) -> list[ContentItem]:
    return supplement_response(lang, id_, 'oratio')


@router.get('/{lang}/api/v5/canticum')
def v5_canticum(lang: str = Depends(validate_locale)) -> Any:
    return supplement_index.get_canticum_index(lang)


@router.get('/{lang}/api/v5/canticum/{id_}', response_model=list[ContentItem])
def v5_canticum_by_id(id_: str, lang: str = Depends(validate_locale)) -> list[ContentItem]:
    return supplement_response(lang, id_, 'canticum')


@router.get('/{lang}/api/v5/icalendar')
@router.get('/{lang}/api/v5/icalendar/{rank}')
def v5_ical(
    rank: int = 2,
    lang: str = Depends(validate_locale),
) -> PlainTextResponse:
    if rank not in range(1, 5):
        rank = 2

    content = controller.get_ical(lang, rank)
    return PlainTextResponse(content, media_type='text/calendar; charset=utf-8')


@router.get('/{lang}/api/v5/version')
def v5_version(lang: str = Depends(validate_locale)) -> dict[str, str]:
    return {"version": __version__.__version__}


# Backwards compatibility for modules that still import `api`.
api = router
