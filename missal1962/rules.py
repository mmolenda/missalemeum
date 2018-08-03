# -*- coding: utf-8 -*-

"""
Rules for solving conflicts between liturgical days occurring at same date
"""
from calendar import isleap

from blocks import FEASTS_OF_JESUS_CLASS_1_AND_2
from constants import SANCTI_12_08, SANCTI_01_13, SANCTI_12_24, TEMPORA_EPI1_0, SANCTI_11_02, SANCTI_11_24, SANCTI_02_24, \
    SANCTI_02_27, PATTERN_TEMPORA, PATTERN_TEMPORA_SUNDAY, PATTERN_SANCTI_CLASS_2, TEMPORA_QUADP3_3, TEMPORA_QUAD6_1, \
    TEMPORA_QUAD6_2, TEMPORA_QUAD6_3, TEMPORA_QUAD6_4, TEMPORA_QUAD6_5, TEMPORA_QUAD6_6, TEMPORA_PASC0_0
from constants import PATTERN_TEMPORA_SUNDAY_CLASS_2, PATTERN_SANCTI_CLASS_1_OR_2

rules = (
    # Immaculate Conception of BMV takes precedence before encountered Advent Sunday.
    (lambda day, ids: SANCTI_12_08 in ids and day.weekday() == 6,
     ((SANCTI_12_08, ), (), ())),

    # Nativity Vigil takes place of 4th Advent Sunday.
    (lambda day, ids: SANCTI_12_24 in ids and day.weekday() == 6,
     ((SANCTI_12_24, ), (), ())),

    # A 1st or 2nd class feast of the Lord occurring on a Sunday
    # takes the place of that Sunday with all rights and privileges;
    # hence there is no commemoration of the Sunday.
    (lambda day, ids: SANCTI_01_13 in ids and TEMPORA_EPI1_0 in ids,
     ((TEMPORA_EPI1_0, ), (), ())),
    (lambda day, ids: set(FEASTS_OF_JESUS_CLASS_1_AND_2).intersection(set(ids)) and
                               any([PATTERN_TEMPORA_SUNDAY_CLASS_2.match(i) for i in ids]),
     ((PATTERN_SANCTI_CLASS_1_OR_2, ), (), ())),

    # St. Matthias the Apostle, normally on Feb 24, but in leap year on Feb 25
    (lambda day, ids: SANCTI_02_24 in ids and isleap(day.year) and day.day == 24,
     ((PATTERN_TEMPORA, ), (), ((2, 25, SANCTI_02_24), ))),

    # Feb 27, normally on Feb 27 but in leap year on Feb 28
    (lambda day, ids: SANCTI_02_27 in ids and isleap(day.year) and day.day == 27,
     ((PATTERN_TEMPORA, ), (), ((2, 28, SANCTI_02_27), ))),

    # All Souls Day; if not Sunday - Nov 2, else Nov 3
    (lambda day, ids: SANCTI_11_02 in ids and day.weekday() == 6,
     ((PATTERN_TEMPORA_SUNDAY, ), (), ((11, 3, SANCTI_11_02), ))),

    # When 2nd class Sunday occurs along with 2nd class feast, the Sunday takes precedence and the feast is commemorated
    (lambda day, ids: any([PATTERN_TEMPORA_SUNDAY_CLASS_2.match(i) for i in ids]) and
                      any([PATTERN_SANCTI_CLASS_2.match(i) for i in ids]),
     ((PATTERN_TEMPORA_SUNDAY_CLASS_2, ), (PATTERN_SANCTI_CLASS_2, ), ())),

    # Ash wednesday and holy week always wins
    (lambda day, ids: {TEMPORA_QUAD6_1,
                       TEMPORA_QUAD6_2,
                       TEMPORA_QUAD6_3,
                       TEMPORA_QUAD6_4,
                       TEMPORA_QUAD6_5,
                       TEMPORA_QUAD6_6,
                       TEMPORA_PASC0_0,
                       TEMPORA_QUADP3_3}.intersection(set(ids)),
     ((PATTERN_TEMPORA, ), (), ())),
)
