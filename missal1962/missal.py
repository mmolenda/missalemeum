# -*- coding: utf-8 -*-

"""
Missal 1962
"""
import re
import sys
import logging
from calendar import isleap
from datetime import date, timedelta
from dateutil.easter import easter

from blocks import POST_EPIPHANY, FROM_PRE_LENT_TO_POST_PENTECOST, WEEK_24_AFTER_PENTECOST, ADVENT, HOLY_NAME, \
    EMBER_DAYS_SEPTEMBER, CHRIST_KING, SUNDAY_IN_CHRISTMAS_OCTAVE, SANCTI
from constants import *
from models import LiturgicalDay, Missal
from rules import rules

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log = logging.getLogger(__name__)


def calc_easter_sunday(year):
    return easter(year)


def calc_holy_family(year):
    """
    Feast of the Holy Family - First Sunday after Epiphany (06 January).
    """
    d = date(year, 1, 6)
    wd = d.weekday()
    delta = 6 - wd if wd < 6 else 7
    return d + timedelta(days=delta)


def calc_septuagesima(year):
    """ Septuagesima Sunday.

    Beginning of the pre-Lenten season (Shrovetide).
    It's 63 days before Ressurection, ninth Sunday before Easter, the third before Ash Wednesday.
    First day of the Ressurection Sunday - related block.
    """
    return calc_easter_sunday(year) - timedelta(days=63)


def calc_first_advent_sunday(year):
    """
    First Sunday of Advent - November 27 if it's Sunday, otherwise closest Sunday.
    """
    d = date(year, 11, 27)
    wd = d.weekday()
    if wd != 6:
        d += timedelta(days=6 - wd)
    return d


def calc_24_sunday_after_pentecost(year):
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
    return calc_first_advent_sunday(year) - timedelta(days=7)


def calc_saturday_before_24_sunday_after_pentecost(year):
    """ Last Saturday before 24th Sunday after Pentecost.

    This is the end of potentially "empty" period that might appear
    between 23rd and 24th Sunday after Pentecost if Easter is early.
    In such case one more Sundays after Epiphany (TEMPORA_EPI*_0) are moved here to "fill the gap"
    """
    return calc_24_sunday_after_pentecost(year) - timedelta(days=1)


def calc_ember_wednesday_september(year):
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


def calc_holy_name(year):
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


def calc_christ_king(year):
    """
    The Feast of Christ the King, last Sunday of October.
    """
    d = date(year, 10, 31)
    while d.month == 10:
        if d.weekday() == 6:
            return d
        d -= timedelta(days=1)


def calc_sunday_christmas_octave(year):
    """
    Sunday within the Octave of Christmas, falls between Dec 26 and Dec 31
    """
    d = date(year, 12, 27)
    while d.year == year:
        if d.weekday() == 6:
            return d
        d += timedelta(days=1)
    return None


def calc_all_souls(year):
    """
    All Souls Day; if not Sunday - Nov 2, else Nov 3
    """
    d = date(year, 11, 2)
    if d.weekday() == 6:
        return date(year, 11, 3)
    return d


def calc_st_matthias(year):
    """
    St. Matthias the Apostle, normally on Feb 24, but in leap year on Feb 25
    """
    return date(year, 2, 24) if not isleap(year) else date(year, 2, 25)


def calc_feb_27(year):
    """
    Feb 27, normally on Feb 27 but in leap year on Feb 28
    """
    return date(year, 2, 27) if not isleap(year) else date(year, 2, 28)


class MissalFactory(object):

    missal = None

    @classmethod
    def create(cls, year):
        cls.missal = Missal(year)
        cls._fill_in_tempora_days(year)
        cls._fill_in_sancti_days()
        cls._fill_in_semi_sancti_days(year)
        cls._resolve_concurrency()
        return cls.missal

    @classmethod
    def _fill_in_tempora_days(cls, year):
        """
        Days depending on variable date, such as Easter or Advent
        """
        # main blocks
        cls._insert_block(
            calc_holy_family(year),
            POST_EPIPHANY)
        cls._insert_block(
            calc_septuagesima(year),
            FROM_PRE_LENT_TO_POST_PENTECOST)
        cls._insert_block(
            calc_saturday_before_24_sunday_after_pentecost(year),
            POST_EPIPHANY,
            reverse=True,
            overwrite=False)
        cls._insert_block(
            calc_24_sunday_after_pentecost(year),
            WEEK_24_AFTER_PENTECOST)
        cls._insert_block(
            calc_first_advent_sunday(year),
            ADVENT,
            stop_date=date(year, 12, 23))
        # additional blocks
        cls._insert_block(
            calc_holy_name(year),
            HOLY_NAME
        )
        cls._insert_block(
            calc_ember_wednesday_september(year),
            EMBER_DAYS_SEPTEMBER)
        cls._insert_block(
            calc_christ_king(year),
            CHRIST_KING
        )
        if calc_sunday_christmas_octave(year):
            cls._insert_block(
                calc_sunday_christmas_octave(year),
                SUNDAY_IN_CHRISTMAS_OCTAVE
            )

    @classmethod
    def _fill_in_sancti_days(cls):
        """
        Days ascribed to a specific date
        """
        for date_, contents in cls.missal.items():
            date_id = date_.strftime("%m-%d")
            days = [LiturgicalDay(ii, date_) for ii in SANCTI
                    if ii.startswith("sancti:{}".format(date_id))]
            contents.extend(days)
            contents.sort(reverse=True)

    @classmethod
    def _fill_in_semi_sancti_days(cls, year):
        """
        Days normally ascribed to a specific date, but in
        certain conditions moved to other dates
        """
        day = calc_all_souls(year)
        cls.missal[day].append(
            LiturgicalDay(SANCTI_11_02_1, day))
        cls.missal[day].sort(reverse=True)

        day = calc_st_matthias(year)
        cls.missal[day].append(LiturgicalDay(SANCTI_02_24_1, day))
        cls.missal[day].sort(reverse=True)

        day = calc_feb_27(year)
        cls.missal[day].append(LiturgicalDay(SANCTI_02_27_1, day))
        cls.missal[day].sort(reverse=True)

    @classmethod
    def _insert_block(cls, start_date, block, stop_date=None,
                      reverse=False, overwrite=True):
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
          datetime.date(2008, 1, 14): [<tempora:epi1-1:4>,
                                       <sancti:01-14_1:3>],
          datetime.date(2008, 1, 15): [<tempora:epi1-2:4',
                                       <sancti:01-15_1:3>],
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
            if cls.missal[index] and not overwrite:
                break
            # break on stop date
            if stop_date == cls.missal[index - timedelta(days=1)]:
                break
            cls.missal[index] = [LiturgicalDay(day_id, index)
                                 for day_id in day_ids]

    @classmethod
    def _resolve_concurrency(cls):
        for day, lit_days in cls.missal.items():
            cls.missal[day] = cls._inner_resolve_concurrency(day, lit_days)

    @classmethod
    def _inner_resolve_concurrency(cls, day, lit_days):
        lit_days_ids = [ld.id for ld in lit_days]
        for condition, patterns in rules:
            if condition(day, lit_days_ids):
                new_days = []
                for pattern in patterns:
                    for lit_day in lit_days:
                        if re.match(pattern, lit_day.id):
                            new_days.append(lit_day)
                return new_days
        return lit_days


if __name__ == '__main__':
    year = int(sys.argv[1]) if len(sys.argv) > 1 else date.today().year
    missal = MissalFactory.create(year)

    for k, v in missal.items():
        if k.weekday() == 6:
            log.info("---")
        log.info("%s %s %s", k.strftime('%A'), k, v)
