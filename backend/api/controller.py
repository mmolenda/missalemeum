import os
import datetime

from functools import lru_cache
from typing import List, Tuple

import ical
from kalendar.factory import MissalFactory
from kalendar.models import Calendar, Day
from propers.models import Proper, ProperConfig
from propers.parser import ProperParser
from utils import get_custom_preface

no_cache = bool(os.environ.get('MISSAL_NO_CACHE'))


@lru_cache(maxsize=0 if no_cache else 64)
def get_calendar(year: int, lang) -> Calendar:
    return MissalFactory().create(year, lang)


@lru_cache(maxsize=0 if no_cache else 512)
def get_day(date_: datetime.date, lang) -> Day:
    missal: Calendar = get_calendar(date_.year, lang)
    return missal.get_day(date_)


def get_proper_by_id(proper_id: str, lang: str) -> Tuple[Proper, Proper]:
    config: ProperConfig = ProperConfig(preface=get_custom_preface(Proper(proper_id, lang)))
    return ProperParser(proper_id, lang, config).parse()


def get_proper_by_date(date_: datetime.date, lang) -> List[Tuple[Proper, Proper]]:
    missal: Calendar = get_calendar(date_.year, lang)
    day: Day = missal.get_day(date_)
    return day.get_proper()


def get_ical(lang, rank=2):
    today = datetime.datetime.now().date()
    current = today - datetime.timedelta(days=90)
    one_year_forward = today + datetime.timedelta(days=365)
    days = {}
    while current <= one_year_forward:
        days[current] = get_day(current, lang)
        current += datetime.timedelta(days=1)
    return ical.IcalBuilder.build(days, rank, lang)
