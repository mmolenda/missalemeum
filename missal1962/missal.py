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

from missal1962 import blocks
from missal1962.constants import *
from missal1962.models import LiturgicalDay, Missal
from missal1962.rules import rules

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log = logging.getLogger(__name__)


def _calc_temporaday__dom_ressurectionis(year):
    """ Dominica Ressurectionis - Easter Sunday """
    return easter(year)

def _calc_temporaday__dom_sanctae_familiae(year):
    """ Dominica Sanctae Familiae Jesu Mariae Joseph

    First Sunday after Epiphany (06 January)
    """
    d = date(year, 1, 6)
    wd = d.weekday()
    delta = 6 - wd if wd < 6 else 7
    return d + timedelta(days=delta)

def _calc_temporaday__dom_septuagesima(year):
    """ Dominica in Septuagesima

    Beginning of the pre-Lenten season
    First day of the Ressurection Sunday - related block.
    It's 63 days before Ressurection.
    """
    return _calc_temporaday__dom_ressurectionis(year) - timedelta(days=63)

def _calc_temporaday__dom_adventus(year):
    """ Dominica I Adventus

    First Sunday of Advent - November 27 if it's Sunday
    or closest Sunday
    """
    d = date(year, 11, 27)
    wd = d.weekday()
    if wd != 6:
        d += timedelta(days=6 - wd)
    return d

def _calc_temporaday__dom_post_pentecost_24(year):
    """ Dominica XXIV Post Pentecosten

    Last Sunday before Dominica I Adventus
    This will be always dom_post_pentecost_24, which will be
    placed either
    * instead of dom_post_pentecost_23 - if number of
      dom_post_pentecost_* == 23)
    * directly after week of dom_post_pentecost_23 - if number of
      dom_post_pentecost_* == 24)
    * directly after week of dom_post_epiphania_6 (moved from post
      epiphania period) - if number of dom_post_pentecost_* > 24)
    """
    return _calc_temporaday__dom_adventus(year) - timedelta(days=7)

def _calc_temporaday__sab_before_dom_post_pentecost_24(year):
    """ Last Saturday before Dominica XXIV Post Pentecosten

    This is the end of potentially "empty" period that might appear
    between Dominica XXIII and Dominica XXIV Post Pentecosten if
    Easter is early. In such case Dominica post Epiphania * are
    moved here to "fill the gap"
    """
    return _calc_temporaday__dom_post_pentecost_24(year) - timedelta(days=1)

def _calc_temporaday__quattour_septembris(year):
    """ Feria Quarta Quattuor Temporum Septembris

    Ember Wednesday in September is a Wednesday after third Sunday
    of September according to John XXIII's motu proprio
    Rubricarum instructum of June 25 1960.
    """
    d = date(year, 9, 1)
    while d.month == 9:
        # third Sunday
        if d.weekday() == 6 and 15 <= d.day <= 21:
            break
        d += timedelta(days=1)
    # Wednesday after third Sunday
    return d + timedelta(days=3)

def _calc_temporaday__sanctissimi_nominis_jesu(year):
    """ Sanctissimi Nominis Jesu

    The Feast of the Holy Name of Jesus. Kept on the First
    Sunday of the year; but if this Sunday falls on
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

def _calc_temporaday__jesu_christi_regis(year):
    """ Jesu Christi Regis

    The Feast of Christ the King, last Sunday of October
    """
    d = date(year, 10, 31)
    while d.month == 10:
        if d.weekday() == 6:
            return d
        d -= timedelta(days=1)

def _calc_temporaday__dom_octavam_nativitatis(year):
    """ Dominica infra octavam Nativitatis

    Sunday within the Octave of Christmas, Sunday between
    Dec 26 and Dec 31
    """
    d = date(year, 12, 27)
    while d.year == year:
        if d.weekday() == 6:
            return d
        d += timedelta(days=1)
    return None

def _calc_sanctiday__11_02_omnium_fidelium_defunctorum(year):
    """ Commemoratione Omnium Fidelium Defunctorum

    All Souls Day; if not Sunday - Nov 2, else Nov 3
    """
    d = date(year, 11, 2)
    if d.weekday() == 6:
        return date(year, 11, 3)
    return d

def _calc_sanctiday__02_24_matthiae_apostoli(year):
    """ Matthiae Apostoli

    saint Matthew the Apostle, normally on Feb 24
    but in leap year on Feb 25
    """
    return date(year, 2, 24) if not isleap(year) else date(year, 2, 25)

def _calc_sanctiday__02_27(year):
    """ Feb 27

    Feb 27, normally on Feb 27
    but in leap year on Feb 28
    """
    return date(year, 2, 27) if not isleap(year) else date(year, 2, 28)


class MissalFactory(object):

    missal = None

    @classmethod
    def create(cls, year):
        cls.missal = Missal(year)
        cls._fill_in_temporaiable_days(year)
        cls._fill_in_sanctied_days()
        cls._fill_in_semi_sanctied_days(year)
        cls._resolve_concurrency()
        return cls.missal

    @classmethod
    def _fill_in_temporaiable_days(cls, year):
        """
        Days depending on temporaiable date, such as Easter or Advent
        """
        # main blocks
        cls._insert_block(
            _calc_temporaday__dom_sanctae_familiae(year),
            blocks.TEMPORADAYS__POST_EPIPHANIA)
        cls._insert_block(
            _calc_temporaday__dom_septuagesima(year),
            blocks.TEMPORADAYS__RESSURECTIONIS)
        cls._insert_block(
            _calc_temporaday__sab_before_dom_post_pentecost_24(year),
            blocks.TEMPORADAYS__POST_EPIPHANIA,
            reverse=True,
            overwrite=False)
        cls._insert_block(
            _calc_temporaday__dom_post_pentecost_24(year),
            blocks.TEMPORADAYS__HEBD_POST_PENTECOST_24)
        cls._insert_block(
            _calc_temporaday__dom_adventus(year),
            blocks.TEMPORADAYS__ADVENT,
            stop_date=date(year, 12, 23))
        # additional blocks
        cls._insert_block(
            _calc_temporaday__sanctissimi_nominis_jesu(year),
            blocks.TEMPORADAYS__SANCTISSIMI_NOMINIS_JESU
        )
        cls._insert_block(
            _calc_temporaday__quattour_septembris(year),
            blocks.TEMPORADAYS__QUATTOUR_SEPTEMBRIS)
        cls._insert_block(
            _calc_temporaday__jesu_christi_regis(year),
            blocks.TEMPORADAYS__JESU_CHRISTI_REGIS
        )
        if _calc_temporaday__dom_octavam_nativitatis(year):
            cls._insert_block(
                _calc_temporaday__dom_octavam_nativitatis(year),
                blocks.TEMPORADAYS__F0_OCTAVAM_NATIVITATIS
            )

    @classmethod
    def _fill_in_sanctied_days(cls):
        """
        Days ascribed to specific date
        """
        for date_, contents in cls.missal.iteritems():
            date_id = date_.strftime("%m_%d")
            days = list(set([LiturgicalDay(ii, date_) for ii in blocks.SANCTIDAYS
                             if ii.startswith("sancti:{}".format(date_id))]))
            contents.extend(days)
            contents.sort(reverse=True)

    @classmethod
    def _fill_in_semi_sanctied_days(cls, year):
        """
        Days normally ascribed to specific date, but in
        certain conditions moved to other dates
        """
        day = _calc_sanctiday__11_02_omnium_fidelium_defunctorum(year)
        cls.missal[day].append(
            LiturgicalDay(SANCTI_11_02_OMNIUM_FIDELIUM_DEFUNCTORUM, day))
        cls.missal[day].sort(reverse=True)

        day = _calc_sanctiday__02_24_matthiae_apostoli(year)
        cls.missal[day].append(LiturgicalDay(SANCTI_02_24_MATTHIAE_APOSTOLI, day))
        cls.missal[day].sort(reverse=True)

        day = _calc_sanctiday__02_27(year)
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
            'tempora:f2_post_epiphania_1:4',
            'tempora:f3_post_epiphania_1:4',
        ]
        Result:
        {
        ...
          datetime.date(2008, 1, 13): [<tempora:epi1-0:2>],
          datetime.date(2008, 1, 14): [<tempora:f2_post_epiphania_1:4>,
                                       <sancti:01-14_1:3>],
          datetime.date(2008, 1, 15): [<tempora:f3_post_epiphania_1:4',
                                       <sancti:01-15_1:3>],
        ...
        }

        Example:
        start_date=2008-11-22, reverse=True
        block = [
            'tempora:f5_post_epiphania_6:4',
            'tempora:f6_post_epiphania_6:4',
            'tempora:sab_post_epiphania_6:4'
        ]
        Result:
        {
        ...
          datetime.date(2008, 11, 20): [<tempora:f5_post_epiphania_6:4>],
          datetime.date(2008, 11, 21): [<tempora:f6_post_epiphania_6:4>],
          datetime.date(2008, 11, 22): [<tempora:sab_post_epiphania_6:4>],
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
        for day, lit_days in cls.missal.iteritems():
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
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 1950
    missal = MissalFactory.create(year)

    for k, v in missal.iteritems():
        if k.weekday() == 6:
            log.info("---")
        log.info("%s %s %s", k.strftime('%A'), k, v)
