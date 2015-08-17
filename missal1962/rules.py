# -*- coding: utf-8 -*-

"""
Rules for solving conflicts between liturgical days occurring at same date
"""
import re
from missal1962 import blocks
from missal1962.constants import *

patterns = {
    'var_dom_adventus': re.compile(r'^var:dom_adventus'),
    'var_dom_2_class': re.compile(r'^var:dom_.*:2$'),
    'fix_1_2_class': re.compile(r'^fix:.*:[12]$')
}

rules = (
    # święto Niepokalanego Poczęcia NMP ma pierwszeństwo przed
    # napotkaną niedzielą Adwentu.
    (lambda day, lit_days_ids: FIX_12_08_CONCEPTIONE_IMMACULATA_BMV in lit_days_ids and day.weekday() == 6,
     (FIX_12_08_CONCEPTIONE_IMMACULATA_BMV, patterns['var_dom_adventus'])),

    # A 1st or 2nd class feast of the Lord occurring on a Sunday
    # takes the place of that Sunday  with all rights and privileges;
    # hence there is no commemoration of the Sunday.
    (lambda day, lit_days_ids: FIX_01_13_BAPTISMATIS_DOMINI in lit_days_ids and VAR_DOM_SANCTAE_FAMILIAE in lit_days_ids,
     (VAR_DOM_SANCTAE_FAMILIAE, )),
    (lambda day, lit_days_ids: set(blocks.DOMINI_1_2).intersection(set(lit_days_ids)) and any([patterns['var_dom_2_class'].match(i) for i in lit_days_ids]),
     (patterns['fix_1_2_class'], )),

    # Nativitatis vigil takes place of 4th Advent Sunday
    (lambda day, lit_days_ids: FIX_12_24_VIGILIA_NATIVITATIS_DOMINI in lit_days_ids and day.weekday() == 6,
     (FIX_12_24_VIGILIA_NATIVITATIS_DOMINI, ))
)