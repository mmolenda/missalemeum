import re
from datetime import date

from missal1962.blocks import EMBER_DAYS, FROM_PRE_LENT_TO_POST_PENTECOST, SANCTI
from missal1962.constants import PATTERN_TEMPORA_SUNDAY_CLASS_2, PATTERN_SANCTI_CLASS_2, PATTERN_ADVENT_FERIA, \
    PATTERN_ADVENT_FERIA_BETWEEN_17_AND_23, PATTERN_TEMPORA_CLASS_3, PATTERN_TEMPORA_CLASS_1, PATTERN_TEMPORA_CLASS_2, \
    PATTERN_SANCTI_CLASS_1, PATTERN_SANCTI_CLASS_3, PATTERN_LENT_SUNDAY, PATTERN_CLASS_1, PATTERN_CLASS_2
from missal1962.missal import MissalFactory
from missal1962.utils import match
from resources.titles_pl import titles


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
            lit_days = lit_day_container.celebration
            if match(lit_days, PATTERN_TEMPORA_CLASS_3) and match(lit_days, [PATTERN_TEMPORA_CLASS_1,
                                                                             PATTERN_TEMPORA_CLASS_2,
                                                                                 PATTERN_SANCTI_CLASS_1,
                                                                             PATTERN_SANCTI_CLASS_2,
                                                                             PATTERN_SANCTI_CLASS_3]):
                print(date_, lit_day_container.celebration)


def match_all_patterns():
    for day_id in  [i[0] for i in FROM_PRE_LENT_TO_POST_PENTECOST] + list(SANCTI):
        if re.match(PATTERN_CLASS_2, day_id):
            print(day_id, titles[day_id])


if __name__ == '__main__':
    # get_year_by_feast_class_and_weekday(1, 6)
    match_all_patterns()

