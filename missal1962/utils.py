import re
from datetime import date

from constants import PATTERN_TEMPORA_SUNDAY_CLASS_2, PATTERN_SANCTI_CLASS_2, PATTERN_ADVENT_FERIA_BETWEEN_17_AND_23
from missal import MissalFactory


def ids(lit_days):
    return [i.id for i in lit_days]


def match(lit_days, patterns):
    if not isinstance(patterns, (list, tuple)):
        patterns = [patterns]
    for lit_day in lit_days:
        for pattern in patterns:
            if re.match(pattern, lit_day.id):
                return lit_day


def get_year_by_date_and_weekday(month, day, weekday):
    """
    Print years where certain date is on specific weekday
    """
    for year in range(1900, 2100):
        if date(year, month, day).weekday() == weekday:
            print(year)


def get_year_by_feast_class_and_weekday(rank, weekday):
    for year in range(1970, 2020):
        missal = MissalFactory.create(year)
        for date_, lit_day_container in missal.items():
            if any([re.match(PATTERN_ADVENT_FERIA_BETWEEN_17_AND_23, i.id) for i in lit_day_container.celebration]) and \
               any([re.match(PATTERN_SANCTI_CLASS_2, i.id) for i in lit_day_container.celebration]):
                print(date_, lit_day_container.celebration)


if __name__ == '__main__':
    get_year_by_feast_class_and_weekday(1, 6)

