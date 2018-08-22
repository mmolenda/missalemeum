# -*- coding: utf-8 -*-

"""
Rules for solving conflicts between liturgical days occurring at same date
"""
import datetime
import re
from calendar import isleap

from blocks import FEASTS_OF_JESUS_CLASS_1_AND_2
from constants import SANCTI_12_08, SANCTI_01_13, SANCTI_12_24, TEMPORA_EPI1_0, SANCTI_11_02, SANCTI_11_24, SANCTI_02_24, \
    SANCTI_02_27, PATTERN_TEMPORA, PATTERN_TEMPORA_SUNDAY, PATTERN_SANCTI_CLASS_2, TEMPORA_QUADP3_3, TEMPORA_QUAD6_1, \
    TEMPORA_QUAD6_2, TEMPORA_QUAD6_3, TEMPORA_QUAD6_4, TEMPORA_QUAD6_5, TEMPORA_QUAD6_6, TEMPORA_PASC0_0
from constants import PATTERN_TEMPORA_SUNDAY_CLASS_2, PATTERN_SANCTI_CLASS_1_OR_2


def ids(lit_days):
    return [i.id for i in lit_days]


def match(lit_days, pattern):
    retval = []
    for lit_day in lit_days:
        if re.match(pattern, lit_day.id):
            retval.append(lit_day)
    return retval


def rule01_immaculate_coneption(day, lit_days):
    # Immaculate Conception of BMV takes precedence before encountered Advent Sunday.
    if SANCTI_12_08 in ids(lit_days) and day.weekday() == 6:
        return match(lit_days, SANCTI_12_08), [], []


def rule02_nativity(day, lit_days):
    # Nativity Vigil takes place of 4th Advent Sunday.
    if SANCTI_12_24 in ids(lit_days) and day.weekday() == 6:
        return match(lit_days, SANCTI_12_24), [], []


def rule03_lord_feast1(day, lit_days):
    # A 1st or 2nd class feast of the Lord occurring on a Sunday
    # takes the place of that Sunday with all rights and privileges;
    # hence there is no commemoration of the Sunday.
    if SANCTI_01_13 in ids(lit_days) and TEMPORA_EPI1_0 in ids(lit_days):
        return match(lit_days, TEMPORA_EPI1_0), [], []


def rule04_lord_feast2(day, lit_days):
    if set(FEASTS_OF_JESUS_CLASS_1_AND_2).intersection(set(ids(lit_days))) and \
            any([PATTERN_TEMPORA_SUNDAY_CLASS_2.match(i) for i in ids(lit_days)]):
        return match(lit_days, PATTERN_SANCTI_CLASS_1_OR_2), [], []


def rule05_st_matthias(day, lit_days):
    # St. Matthias the Apostle, normally on Feb 24, but in leap year on Feb 25
    if SANCTI_02_24 in ids(lit_days) and isleap(day.year) and day.day == 24:
        return match(lit_days, PATTERN_TEMPORA), [], [[datetime.date(day.year, 2, 25), match(lit_days, SANCTI_02_24)]]


def rule06_feb27(day, lit_days):
    # Feb 27, normally on Feb 27 but in leap year on Feb 28
    if SANCTI_02_27 in ids(lit_days) and isleap(day.year) and day.day == 27:
        return match(lit_days, PATTERN_TEMPORA), [], [[datetime.date(day.year, 2, 28), match(lit_days, SANCTI_02_27)]]


def rule07_all_souls(day, lit_days):
    # All Souls Day; if not Sunday - Nov 2, else Nov 3
    if SANCTI_11_02 in ids(lit_days) and day.weekday() == 6:
        return match(lit_days, PATTERN_TEMPORA_SUNDAY), [], [[datetime.date(day.year, 11, 3), match(lit_days, SANCTI_11_02)]]


def rule08_2nd_class_sunday(day, lit_days):
    # When 2nd class Sunday occurs along with 2nd class feast, the Sunday takes precedence and the feast is commemorated
    if any([PATTERN_TEMPORA_SUNDAY_CLASS_2.match(i) for i in ids(lit_days)]) and \
            any([PATTERN_SANCTI_CLASS_2.match(i) for i in ids(lit_days)]):
        return match(lit_days, PATTERN_TEMPORA_SUNDAY_CLASS_2), match(lit_days, PATTERN_SANCTI_CLASS_2), []


def rule09_1st_class_feria(day, lit_days):
    # Ash wednesday and holy week always wins
    if {TEMPORA_QUAD6_1,
        TEMPORA_QUAD6_2,
        TEMPORA_QUAD6_3,
        TEMPORA_QUAD6_4,
        TEMPORA_QUAD6_5,
        TEMPORA_QUAD6_6,
        TEMPORA_PASC0_0,
        TEMPORA_QUADP3_3}.intersection(set(ids(lit_days))):
        return match(lit_days, PATTERN_TEMPORA), [], []
