# -*- coding: utf-8 -*-

"""
Missal 1962
"""
from collections import defaultdict

import importlib
from copy import copy
from datetime import date, timedelta
from dateutil.easter import easter
from typing import List, Tuple, Union

from missal1962.models import LiturgicalDay, Missal
from missal1962.rules import rules


class MissalFactory(object):

    missal = None
    lang = None
    blocks = None

    @classmethod
    def create(cls, year: int, lang: str='Polski') -> Missal:
        cls.lang = lang
        cls.blocks = importlib.import_module(f'resources.{cls.lang}.blocks')
        cls.missal: Missal = Missal(year, cls.lang)
        cls._fill_in_tempora_days(year)
        cls._fill_in_sancti_days()
        cls._resolve_concurrency()
        return cls.missal

    @classmethod
    def _fill_in_tempora_days(cls, year: int):
        """
        Days depending on variable date, such as Easter or Advent
        """

        # main blocks
        cls._insert_block(cls.calc_holy_family(year), cls.blocks.POST_EPIPHANY)
        cls._insert_block(cls.calc_septuagesima(year), cls.blocks.FROM_PRE_LENT_TO_POST_PENTECOST)
        cls._insert_block(cls.calc_saturday_before_24_sunday_after_pentecost(year), cls.blocks.POST_EPIPHANY,
                          reverse=True, overwrite=False)
        cls._insert_block(cls.calc_24_sunday_after_pentecost(year), cls.blocks.WEEK_24_AFTER_PENTECOST)
        cls._insert_block(cls.calc_first_advent_sunday(year), cls.blocks.ADVENT, stop_date=date(year, 12, 23))
        # additional blocks
        cls._insert_block(cls.calc_holy_name(year), cls.blocks.HOLY_NAME)
        cls._insert_block(cls.calc_ember_wednesday_september(year), cls.blocks.EMBER_DAYS_SEPTEMBER)
        cls._insert_block(cls.calc_christ_king(year), cls.blocks.CHRIST_KING)
        if cls.calc_sunday_christmas_octave(year):
            cls._insert_block(cls.calc_sunday_christmas_octave(year), cls.blocks.SUNDAY_IN_CHRISTMAS_OCTAVE)

    @classmethod
    def _fill_in_sancti_days(cls):
        """
        Days ascribed to a specific date
        """
        for date_, lit_day_container in cls.missal.items():
            date_id = date_.strftime("%m-%d")
            days = [LiturgicalDay(ii, date_, cls.lang) for ii in cls.blocks.SANCTI if ii.startswith("sancti:{}".format(date_id))]
            lit_day_container.celebration.extend(days)
            lit_day_container.celebration.sort(reverse=True)

    @classmethod
    def _insert_block(cls, start_date: date, block: tuple, stop_date: date = None,
                      reverse: bool = False, overwrite: bool = True):
        """ Insert a block of related `LiturgicalDay` objects.

        :param start_date: date where first or last (if `reverse`=True)
                           element of the block will be inserted
        :type start_date: date object
        :param block: list of day identifiers in established order
        :type block: list of strings
        :param stop_date: last date to insert block element
        :type stop_date: date object
        :param reverse: if False, identifiers will be put in days
                        following `start_date` otherwise they'll
                        be put in leading up days
        :param overwrite: if True, overwrite existing identifiers,
                          else quit on first non empty day

        Example:
        start_date=2008-01-13, reverse=False
        block = [
            'tempora:epi1-0:2',
            'tempora:epi1-1:4',
            'tempora:epi1-2:4',
        ]
        Result:
        {
        ...
          datetime.date(2008, 1, 13): [<tempora:epi1-0:2>],
          datetime.date(2008, 1, 14): [<tempora:epi1-1:4>],
          datetime.date(2008, 1, 15): [<tempora:epi1-2:4'],
        ...
        }

        Example:
        start_date=2008-11-22, reverse=True
        block = [
            'tempora:epi6-3:4',
            'tempora:epi6-4:4',
            'tempora:epi6-5:4'
        ]
        Result:
        {
        ...
          datetime.date(2008, 11, 20): [<tempora:epi6-3:4>],
          datetime.date(2008, 11, 21): [<tempora:epi6-4:4>],
          datetime.date(2008, 11, 22): [<tempora:epi6-5:4>],
        ...
        }
        """
        if reverse:
            block = reversed(block)
        for ii, day_ids in enumerate(block):
            index = start_date + timedelta(days=ii if not reverse else -ii)
            # skip on empty day in a block
            if not day_ids:
                continue
            # break on first non-empty day
            if cls.missal[index].celebration and not overwrite:
                break
            # break on stop date
            if stop_date == index - timedelta(days=1):
                break
            cls.missal[index].tempora = [LiturgicalDay(day_id, index, cls.lang) for day_id in day_ids]
            cls.missal[index].celebration = copy(cls.missal[index].tempora)

    @classmethod
    def _resolve_concurrency(cls):
        shifted_all = defaultdict(list)
        for date_, lit_day_container in cls.missal.items():
            celebration, commemoration, shifted = cls._apply_rules(date_, shifted_all.pop(date_, []))
            cls.missal[date_].celebration = celebration
            cls.missal[date_].commemoration = commemoration
            for k, v in shifted:
                shifted_all[k].extend(v)

    @classmethod
    def _apply_rules(cls,
                     date_: date,
                     shifted: List[LiturgicalDay]) -> \
            Tuple[List[LiturgicalDay], List[LiturgicalDay], List[LiturgicalDay]]:
        for rule in rules:
            results = rule(cls.missal,
                           date_,
                           cls.missal[date_].tempora,
                           cls.missal[date_].celebration + shifted,
                           cls.lang)
            if results is None or not any(results):
                continue
            return results
        return cls.missal[date_].celebration, [], []

    @classmethod
    def calc_easter_sunday(cls, year: int) -> date:
        return easter(year)

    @classmethod
    def calc_holy_family(cls, year: int) -> date:
        """
        Feast of the Holy Family - First Sunday after Epiphany (06 January).
        """
        d = date(year, 1, 6)
        wd = d.weekday()
        delta = 6 - wd if wd < 6 else 7
        return d + timedelta(days=delta)

    @classmethod
    def calc_septuagesima(cls, year: int) -> date:
        """ Septuagesima Sunday.

        Beginning of the pre-Lenten season (Shrovetide).
        It's 63 days before Ressurection, ninth Sunday before Easter, the third before Ash Wednesday.
        First day of the Ressurection Sunday - related block.
        """
        return cls.calc_easter_sunday(year) - timedelta(days=63)

    @classmethod
    def calc_first_advent_sunday(cls, year: int) -> date:
        """
        First Sunday of Advent - November 27 if it's Sunday, otherwise closest Sunday.
        """
        d = date(year, 11, 27)
        wd = d.weekday()
        if wd != 6:
            d += timedelta(days=6 - wd)
        return d

    @classmethod
    def calc_24_sunday_after_pentecost(cls, year: int) -> date:
        """ 24th Sunday after Pentecost.

        Last Sunday before First Sunday of Advent.
        It will be always TEMPORA_PENT24_0, which will be placed either:
        * instead of TEMPORA_PENT23_0
          if the number of TEMPORA_PENT*_0 Sundays in given year == 23)
        * directly after a week starting with TEMPORA_PENT23_0
          if the number of TEMPORA_PENT*_0 Sundays in given year == 24)
        * directly after a week starting with TEMPORA_EPI6_0 (moved from post-epiphania period)
          if the number of TEMPORA_PENT*_0 Sundays in given year > 24)
        """
        return cls.calc_first_advent_sunday(year) - timedelta(days=7)

    @classmethod
    def calc_saturday_before_24_sunday_after_pentecost(cls, year: int) -> date:
        """ Last Saturday before 24th Sunday after Pentecost.

        This is the end of potentially "empty" period that might appear
        between 23rd and 24th Sunday after Pentecost if Easter is early.
        In such case one or more Sundays after Epiphany (TEMPORA_EPI*_0) are moved here to "fill the gap"
        """
        return cls.calc_24_sunday_after_pentecost(year) - timedelta(days=1)

    @classmethod
    def calc_ember_wednesday_september(cls, year: int) -> date:
        """ Wednesday of the Ember Days of September.

        Ember Wednesday in September is a Wednesday after third Sunday
        of September according to John XXIII's motu proprio
        "Rubricarum instructum" of June 25 1960.
        """
        d = date(year, 9, 1)
        while d.month == 9:
            # third Sunday
            if d.weekday() == 6 and 15 <= d.day <= 21:
                break
            d += timedelta(days=1)
        # Wednesday after third Sunday
        return d + timedelta(days=3)

    @classmethod
    def calc_holy_name(cls, year: int) -> date:
        """ The Feast of the Holy Name of Jesus.

        Kept on the First Sunday of the year; but if this Sunday falls on
        1st, 6th or 7th January, the feast is kept on 2nd January.
        """
        d = date(year, 1, 1)
        while d.day <= 7:
            wd = d.weekday()
            if d.day in (1, 6, 7) and wd == 6:
                return date(year, 1, 2)
            if wd == 6:
                return d
            d += timedelta(days=1)

    @classmethod
    def calc_christ_king(cls, year: int) -> date:
        """
        The Feast of Christ the King, last Sunday of October.
        """
        d = date(year, 10, 31)
        while d.month == 10:
            if d.weekday() == 6:
                return d
            d -= timedelta(days=1)

    @classmethod
    def calc_sunday_christmas_octave(cls, year: int) -> Union[date, None]:
        """
        Sunday within the Octave of Christmas, falls between Dec 26 and Dec 31
        """
        d = date(year, 12, 27)
        while d.year == year:
            if d.weekday() == 6:
                return d
            d += timedelta(days=1)
        return None
