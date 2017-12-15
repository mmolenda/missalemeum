# -*- coding: utf-8 -*-

"""
Rules for solving conflicts between liturgical days occurring at same date
"""
import re
from missal1962 import blocks
from missal1962.constants import *

patterns = {
    'tempora_dom_adventus': re.compile(r'^tempora:dom_adventus'),
    'tempora_dom_2_class': re.compile(r'^tempora:dom_.*:2$'),
    'sancti_1_2_class': re.compile(r'^sancti:.*:[12]$')
}

rules = (
    # święto Niepokalanego Poczęcia NMP ma pierwszeństwo przed
    # napotkaną niedzielą Adwentu.
    (lambda day, lit_days_ids: SANCTI_12_08_CONCEPTIONE_IMMACULATA_BMV in lit_days_ids and day.weekday() == 6,
     (SANCTI_12_08_CONCEPTIONE_IMMACULATA_BMV, patterns['tempora_dom_adventus'])),

    # A 1st or 2nd class feast of the Lord occurring on a Sunday
    # takes the place of that Sunday  with all rights and privileges;
    # hence there is no commemoration of the Sunday.
    (lambda day, lit_days_ids: SANCTI_01_13_BAPTISMATIS_DOMINI in lit_days_ids and TEMPORA_EPI1_0 in lit_days_ids,
     (TEMPORA_EPI1_0,)),
    (lambda day, lit_days_ids: set(blocks.DOMINI_1_2).intersection(set(lit_days_ids)) and any([patterns['tempora_dom_2_class'].match(i) for i in lit_days_ids]),
     (patterns['sancti_1_2_class'], )),

    # Nativitatis vigil takes place of 4th Advent Sunday
    (lambda day, lit_days_ids: SANCTI_12_24_VIGILIA_NATIVITATIS_DOMINI in lit_days_ids and day.weekday() == 6,
     (SANCTI_12_24_VIGILIA_NATIVITATIS_DOMINI, ))
)