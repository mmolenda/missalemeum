
import json
import os
from datetime import datetime, date

import pytest

from missal1962.constants import *
from missal1962.missal import MissalFactory
from missal1962.models import LiturgicalDay


HERE = os.path.abspath(os.path.dirname(__file__))


def _to_date_obj(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None


with open(os.path.join(HERE, 'tempora_fixtures.json')) as fh:
    expected = json.load(fh)


@pytest.mark.parametrize("year,dates", sorted(expected.items()))
def test_tempora(year, dates):
    missal = MissalFactory.create(int(year))
    assert _to_date_obj(dates[0]) == missal.get_day(TEMPORA_QUADP1_0)[0]
    assert _to_date_obj(dates[1]) == missal.get_day(TEMPORA_QUADP3_3)[0]
    assert _to_date_obj(dates[2]) == missal.get_day(TEMPORA_PASC0_0)[0]
    assert _to_date_obj(dates[3]) == missal.get_day(TEMPORA_PASC5_4)[0]
    assert _to_date_obj(dates[4]) == missal.get_day(TEMPORA_PASC7_0)[0]
    assert _to_date_obj(dates[5]) == missal.get_day(TEMPORA_PENT01_4)[0]
    assert _to_date_obj(dates[6]) == missal.get_day(TEMPORA_ADV1_0)[0]
    # TEMPORA_EPI4_0 might not exist in given year, then None is returned
    actual = missal.get_day(TEMPORA_EPI4_0)[0] if \
        missal.get_day(TEMPORA_EPI4_0) else None
    assert _to_date_obj(dates[7]) == actual
    assert _to_date_obj(dates[8]) == missal.get_day(TEMPORA_PENT_6)[0]
    assert _to_date_obj(dates[9]) == missal.get_day(NAT2_0)[0]
    assert _to_date_obj(dates[10]) == missal.get_day(SANCTI_10_DUr)[0]
    # NAT1_0 might not exist in given year, then None is returned
    actual = missal.get_day(NAT1_0)[0] if \
        missal.get_day(NAT1_0) else None
    assert _to_date_obj(dates[11]) == actual


@pytest.mark.parametrize("day_id,expected_date", [
    # All Souls Day; if not Sunday - Nov 2, else Nov 3
    (SANCTI_11_02, (2008, 11, 3)),
    (SANCTI_11_02, (2014, 11, 3)),
    (SANCTI_11_02, (2015, 11, 2)),
    (SANCTI_11_02, (2063, 11, 2)),
    # Days dependent on a leap year
    (SANCTI_02_24, (2012, 2, 25)),
    (SANCTI_02_27, (2012, 2, 28)),
    (SANCTI_02_24, (2016, 2, 25)),
    (SANCTI_02_27, (2016, 2, 28)),
    (SANCTI_02_24, (2017, 2, 24)),
    (SANCTI_02_27, (2017, 2, 27)),
    (SANCTI_02_24, (2018, 2, 24)),
    (SANCTI_02_27, (2018, 2, 27))
])
def test_sancti_shifted(day_id, expected_date):
    assert MissalFactory.create(expected_date[0]).get_day(day_id)[0] == date(*expected_date)


@pytest.mark.parametrize("date_,expected_day_ids", [
    # Dec 08 Immaculate Conception of BVM
    ((1907, 12, 8), [SANCTI_12_08]),
    ((1912, 12, 8), [SANCTI_12_08]),
    ((1913, 12, 8), [SANCTI_12_08]),
    # 1 and 2 class feasts of the Lord occurring on Sunday of 2 class
    ((2013, 1, 6), [SANCTI_01_06]),
    ((2036, 1, 6), [SANCTI_01_06]),
    ((2013, 1, 13), [TEMPORA_EPI1_0]),
    ((2036, 1, 13), [TEMPORA_EPI1_0]),
    ((1911, 8, 6), [SANCTI_08_06]),
    ((1922, 8, 6), [SANCTI_08_06]),
    # Nativity_vigil
    ((1950, 12, 24), [SANCTI_12_24]),
    ((2000, 12, 24), [SANCTI_12_24])
])
def test_given_date_contains_proper_day_ids(date_, expected_day_ids):
    assert [i.id for i in MissalFactory.create(date_[0])[date(*date_)].celebration] == expected_day_ids


@pytest.mark.parametrize("date_,expected_celebration,expected_commemoration", [
    # occurence of 2nd class sunday and 2nd class feast
    ((1996, 9, 8), [TEMPORA_PENT15_0], [SANCTI_09_08]),
    ((2009, 7, 26), [TEMPORA_PENT08_0], [SANCTI_07_26]),
    ((2019, 9, 15), [TEMPORA_PENT14_0], [SANCTI_09_15]),
    ((2018, 10, 7), [TEMPORA_PENT20_0], [SANCTI_10_07]),
    # ash wednesday and weeks of holy week always win
    ((2008, 2, 6), [TEMPORA_QUADP3_3], []),
    ((2011, 3, 9), [TEMPORA_QUADP3_3], []),
    ((2012, 2, 22), [TEMPORA_QUADP3_3], []),
    ((2015, 2, 18), [TEMPORA_QUADP3_3], []),
    ((2044, 4, 11), [TEMPORA_QUAD6_1], []),
    ((2018, 3, 27), [TEMPORA_QUAD6_2], []),
    ((2044, 4, 13), [TEMPORA_QUAD6_3], []),
    ((2044, 4, 14), [TEMPORA_QUAD6_4], []),
    ((1952, 4, 11), [TEMPORA_QUAD6_5], []),
    ((1954, 4, 17), [TEMPORA_QUAD6_6], []),
    ((1960, 4, 17), [TEMPORA_PASC0_0], []),
    # advent feria 17-24, ember days of lent, september and advent give away to 2nd class feast
    ((2018, 2, 24), [SANCTI_02_24], [TEMPORA_QUAD1_6]),
    ((1972, 2, 25), [SANCTI_02_24], [TEMPORA_QUAD1_5]),
    ((2019, 9, 21), [SANCTI_09_21], [TEMPORA_PENT_6]),
    ((2018, 12, 21), [SANCTI_12_21], [TEMPORA_ADV3_5]),
])
def test_conflicts(date_, expected_celebration, expected_commemoration):
    missal = MissalFactory.create(date_[0])
    assert [i.id for i in missal[date(*date_)].celebration] == expected_celebration
    assert [i.id for i in missal[date(*date_)].commemoration] == expected_commemoration


@pytest.mark.parametrize("day_id,date_,expected_weekday", [
    (TEMPORA_EPI2_3, (2002, 1, 23), 2),
    (TEMPORA_QUADP1_0, (2002, 1, 27), 6),
    (TEMPORA_QUADP1_0, (2002, 1, 28), 6)
])
def test_liturgical_days_fall_in_proper_weedays(day_id, date_, expected_weekday):
    assert LiturgicalDay(day_id, date(*date_)).weekday == expected_weekday


@pytest.mark.parametrize("day_id,date_,expected_rank", [
    # Days with unchanged ranks
    (TEMPORA_EPI2_3, (2002, 1, 23), 4),
    (TEMPORA_QUADP1_0, (2002, 1, 27), 2),
    # Advent 2002 - increased ranks of feria days from Dec 17
    (TEMPORA_ADV3_1, (2002, 12, 16), 3),
    (TEMPORA_ADV3_2, (2002, 12, 17), 2),
    (TEMPORA_ADV3_3, (2002, 12, 18), 2),
    (TEMPORA_ADV3_4, (2002, 12, 19), 2),
    (TEMPORA_ADV3_5, (2002, 12, 20), 2),
    (TEMPORA_ADV3_6, (2002, 12, 21), 2),
    (TEMPORA_ADV4_0, (2002, 12, 22), 1),
    (TEMPORA_ADV4_1, (2002, 12, 23), 2),
    # Advent 2015 - increased ranks of feria days from Dec 17
    (TEMPORA_ADV3_2, (2015, 12, 15), 3),
    (TEMPORA_ADV3_3, (2015, 12, 16), 2),
    (TEMPORA_ADV3_4, (2015, 12, 17), 2),
    (TEMPORA_ADV3_5, (2015, 12, 18), 2),
    (TEMPORA_ADV3_6, (2015, 12, 19), 2),
    (TEMPORA_ADV4_0, (2015, 12, 20), 1),
    (TEMPORA_ADV4_1, (2015, 12, 21), 2),
    (TEMPORA_ADV4_2, (2015, 12, 22), 2),
    (TEMPORA_ADV4_3, (2015, 12, 23), 2)
])
def test_liturgical_days_have_proper_ranks(day_id, date_, expected_rank):
    assert LiturgicalDay(day_id, date(*date_)).rank == expected_rank


def test_liturgical_day_compare():
    rank_1_1 = LiturgicalDay(TEMPORA_PASC7_0, date(2015, 5, 24))
    rank_1_2 = LiturgicalDay(SANCTI_11_01, date(2015, 11, 1))
    rank_2_1 = LiturgicalDay(TEMPORA_EPI1_0, date(2015, 1, 11))
    rank_2_2 = LiturgicalDay(SANCTI_01_13, date(2015, 1, 13))
    rank_3_1 = LiturgicalDay(TEMPORA_QUAD5_5, date(2015, 3, 27))
    rank_3_2 = LiturgicalDay(SANCTI_03_28, date(2015, 3, 28))
    rank_4_1 = LiturgicalDay(TEMPORA_PENT01_1, date(2015, 6, 1))
    rank_4_2 = LiturgicalDay(SANCTI_08_09, date(2015, 8, 9))

    assert rank_1_1 == rank_1_2
    assert rank_1_1 >= rank_1_2
    assert rank_1_1 <= rank_1_2
    assert rank_1_1 != rank_2_1
    assert rank_1_1 > rank_2_1
    assert rank_1_1 > rank_3_1
    assert rank_1_1 > rank_4_1

    assert rank_2_1 < rank_1_1
    assert rank_2_1 == rank_2_2
    assert rank_2_1 >= rank_2_2
    assert rank_2_1 <= rank_2_2
    assert rank_2_1 != rank_3_2
    assert rank_2_1 > rank_3_1
    assert rank_2_1 > rank_4_1

    assert rank_3_1 < rank_1_1
    assert rank_3_1 < rank_2_1
    assert rank_3_1 == rank_3_2
    assert rank_3_1 >= rank_3_2
    assert rank_3_1 <= rank_3_2
    assert rank_3_1 != rank_4_1
    assert rank_3_1 > rank_4_1

    assert rank_4_1 < rank_1_1
    assert rank_4_1 < rank_2_1
    assert rank_4_1 < rank_3_1
    assert rank_4_1 != rank_3_1
    assert rank_4_1 < rank_4_2
    assert rank_4_1 >= rank_4_2
    assert rank_4_1 <= rank_4_2
