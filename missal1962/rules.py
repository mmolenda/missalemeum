# -*- coding: utf-8 -*-

"""
Rules for solving conflicts between liturgical days occurring at same date
"""

from blocks import FEASTS_OF_JESUS_CLASS_1_AND_2
from constants import *
from models import patterns

rules = (
    # Immaculate Conception of BMV takes precedence before encountered Advent Sunday.
    (lambda day, lit_days_ids: SANCTI_12_08 in lit_days_ids and day.weekday() == 6,
     (SANCTI_12_08, patterns['advent-sunday'])),

    # A 1st or 2nd class feast of the Lord occurring on a Sunday
    # takes the place of that Sunday with all rights and privileges;
    # hence there is no commemoration of the Sunday.
    (lambda day, lit_days_ids: SANCTI_01_13 in lit_days_ids and TEMPORA_EPI1_0 in lit_days_ids,
     (TEMPORA_EPI1_0,)),
    (lambda day, lit_days_ids: set(FEASTS_OF_JESUS_CLASS_1_AND_2).intersection(set(lit_days_ids)) and
                               any([patterns['tempora-sunday-class-2'].match(i) for i in lit_days_ids]),
     (patterns['sancti-sunday-class-1-or-2'], )),

    # Nativity Vigil takes place of 4th Advent Sunday.
    (lambda day, lit_days_ids: SANCTI_12_24 in lit_days_ids and day.weekday() == 6,
     (SANCTI_12_24, ))
)
