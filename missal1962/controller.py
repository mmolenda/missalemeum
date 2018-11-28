import datetime

from functools import lru_cache
from typing import Iterator, List, Tuple

from kalendar.factory import MissalFactory
from kalendar.models import Calendar, Day
from propers.models import Proper
from propers.parser import ProperParser


@lru_cache(maxsize=32)
def get_calendar(year: int, lang) -> Calendar:
    return MissalFactory.create(year, lang)


@lru_cache(maxsize=32)
def get_proper_by_id(proper_id: str, lang: str) -> Tuple[Proper, Proper]:
    return ProperParser.parse(proper_id.lower().replace('__', ':'), lang)


@lru_cache(maxsize=32)
def get_proper_by_date(date_: datetime.date, lang) -> List[Tuple[Proper, Proper]]:
    missal: Calendar = get_calendar(date_.year, lang)
    day: Day = missal.get_day(date_)
    return day.get_proper()