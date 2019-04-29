import os
import datetime

from functools import lru_cache
from typing import List, Tuple

from kalendar.factory import MissalFactory
from kalendar.models import Calendar, Day
from propers.models import Proper, ProperConfig
from propers.parser import ProperParser
from utils import infer_custom_preface

no_cache = bool(os.environ.get('MISSAL_NO_CACHE'))


@lru_cache(maxsize=0 if no_cache else 64)
def get_calendar(year: int, lang) -> Calendar:
    return MissalFactory.create(year, lang)


def get_proper_by_id(proper_id: str, lang: str) -> Tuple[Proper, Proper]:
    config: ProperConfig = ProperConfig(preface=infer_custom_preface(Proper(proper_id)))
    return ProperParser.parse(proper_id.lower().replace('__', ':'), lang, config)


def get_proper_by_date(date_: datetime.date, lang) -> List[Tuple[Proper, Proper]]:
    missal: Calendar = get_calendar(date_.year, lang)
    day: Day = missal.get_day(date_)
    return day.get_proper()
