import re
from datetime import date

from constants import PATTERN_TEMPORA_SUNDAY_CLASS_2, PATTERN_SANCTI_CLASS_2
from missal import MissalFactory


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
            if any([re.match(PATTERN_TEMPORA_SUNDAY_CLASS_2, i.id) for i in lit_day_container.celebration]) and \
               any([re.match(PATTERN_SANCTI_CLASS_2, i.id) for i in lit_day_container.celebration]):
                print(date_, lit_day_container.celebration)


if __name__ == '__main__':
    get_year_by_feast_class_and_weekday(1, 6)
