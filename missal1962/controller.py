import datetime
import importlib
from collections import namedtuple
from typing import Iterator, List, Tuple

from kalendar.factory import MissalFactory
from kalendar.models import Calendar, Day
from propers.models import Proper
from propers.parser import ProperParser


def get_calendar(year: int, lang) -> Calendar:
    return MissalFactory.create(year, lang)


def get_proper_by_id(proper_id: str, lang: str) -> Tuple[Proper, Proper]:
    return ProperParser.parse(proper_id.lower().replace('__', ':'), lang)


def get_proper_by_date(date_: datetime.date, lang) -> List[Tuple[Proper, Proper]]:
    missal: Calendar = get_calendar(date_.year, lang)
    day: Day = missal.get_day(date_)
    return day.get_proper()


def search(search_string: str, lang: str) -> Iterator[namedtuple]:
    titles = importlib.import_module(f'constants.{lang}.translation')
    Result = namedtuple('Result', 'id title')
    for id_, title in titles.titles.items():
        if search_string.strip().lower() in title.lower():
            yield Result(id=':'.join(id_.split(':')[:2]), title=title)
