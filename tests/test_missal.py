
import json
import os
from datetime import datetime, date

import pytest

from missal1962 import constants as c
from missal1962.models import LiturgicalDay
from missal1962 import match
from tests.conftest import get_missal

HERE = os.path.abspath(os.path.dirname(__file__))


def _to_date_obj(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None


with open(os.path.join(HERE, 'tempora_fixtures.json')) as fh:
    expected = json.load(fh)


@pytest.mark.parametrize("year,dates", sorted(expected.items()))
def test_tempora(year, dates):
    missal = get_missal(int(year))
    assert _to_date_obj(dates[0]) == missal.get_day(c.TEMPORA_QUADP1_0)[0]
    assert _to_date_obj(dates[1]) == missal.get_day(c.TEMPORA_QUADP3_3)[0]
    assert _to_date_obj(dates[2]) == missal.get_day(c.TEMPORA_PASC0_0)[0]
    assert _to_date_obj(dates[3]) == missal.get_day(c.TEMPORA_PASC5_4)[0]
    assert _to_date_obj(dates[4]) == missal.get_day(c.TEMPORA_PASC7_0)[0]
    assert _to_date_obj(dates[5]) == missal.get_day(c.TEMPORA_PENT01_4)[0]
    assert _to_date_obj(dates[6]) == missal.get_day(c.TEMPORA_ADV1_0)[0]
    # TEMPORA_EPI4_0 might not exist in given year, then None is returned
    actual = missal.get_day(c.TEMPORA_EPI4_0)[0] if \
        missal.get_day(c.TEMPORA_EPI4_0) else None
    assert _to_date_obj(dates[7]) == actual
    assert _to_date_obj(dates[8]) == missal.get_day(c.TEMPORA_PENT_6)[0]
    assert _to_date_obj(dates[9]) == missal.get_day(c.NAT2_0)[0]
    assert _to_date_obj(dates[10]) == missal.get_day(c.SANCTI_10_DUr)[0]
    # NAT1_0 might not exist in given year, then None is returned
    actual = missal.get_day(c.NAT1_0)[0] if \
        missal.get_day(c.NAT1_0) else None
    assert _to_date_obj(dates[11]) == actual


@pytest.mark.parametrize("day_id,expected_date", [
    # All Souls Day; if not Sunday - Nov 2, else Nov 3
    (c.SANCTI_11_02, (2008, 11, 3)),
    (c.SANCTI_11_02, (2014, 11, 3)),
    (c.SANCTI_11_02, (2015, 11, 2)),
    (c.SANCTI_11_02, (2063, 11, 2)),
    # Days dependent on a leap year
    (c.SANCTI_02_24, (2012, 2, 25)),
    (c.SANCTI_02_27, (2012, 2, 28)),
    (c.SANCTI_02_24, (2016, 2, 25)),
    (c.SANCTI_02_24, (2017, 2, 24)),
    (c.SANCTI_02_27, (2017, 2, 27)),
    (c.SANCTI_02_24, (2018, 2, 24)),
    (c.SANCTI_02_27, (2018, 2, 27)),
    # St Joseph
    (c.SANCTI_03_19, (2023, 3, 20)),
    (c.SANCTI_03_19, (2028, 3, 20)),
    (c.SANCTI_03_19, (2000, 3, 20)),
    # Annunciation
    (c.SANCTI_03_25, (2018, 4, 9)),
    (c.SANCTI_03_25, (2027, 4, 5)),
    (c.SANCTI_03_25, (2057, 3, 26)),
    # St Joseph worker
    (c.SANCTI_05_01, (2038, 5, 3)),
    # St. John Baptist
    (c.SANCTI_06_24, (2022, 6, 25)),
    (c.SANCTI_06_24, (2033, 6, 25)),
    # Ss. Peter and Paul
    (c.SANCTI_06_29, (2057, 6, 30)),
    (c.SANCTI_06_29, (2068, 6, 30)),


])
def test_sancti_shifted(day_id, expected_date):
    assert get_missal(expected_date[0]).get_day(day_id)[0] == date(*expected_date)


@pytest.mark.parametrize("date_,celebration,commemoration", [
    ((1907, 12, 8), [c.SANCTI_12_08], []),
    ((1912, 12, 8), [c.SANCTI_12_08], []),
    ((1913, 12, 8), [c.SANCTI_12_08], []),
    # 1 and 2 class feasts of the Lord occurring on Sunday of 2 class
    ((2013, 1, 6), [c.SANCTI_01_06], []),
    ((2036, 1, 6), [c.SANCTI_01_06], []),
    ((2013, 1, 13), [c.TEMPORA_EPI1_0], []),
    ((2036, 1, 13), [c.TEMPORA_EPI1_0], []),
    ((1911, 8, 6), [c.SANCTI_08_06], []),
    ((1922, 8, 6), [c.SANCTI_08_06], []),
    # Nativity_vigil
    ((1950, 12, 24), [c.SANCTI_12_24], []),
    ((2000, 12, 24), [c.SANCTI_12_24], []),
    # Commemorations
    ((2018, 2, 15), [c.TEMPORA_QUADP3_4], [c.SANCTI_02_15]),
    ((2018, 4, 22), [c.TEMPORA_PASC3_0], []),
    ((2018, 4, 25), [c.SANCTI_04_25], []),  # St. Mark, Evangelist
    ((2018, 5, 10), [c.TEMPORA_PASC5_4], []),  # Ascension, no comm.
    ((2018, 5, 19), [c.TEMPORA_PASC6_6], []),  # Vigil of Pentecost, no comm.
    ((2018, 5, 21), [c.TEMPORA_PASC7_1], []),  # Pentecost Octave, no comm.
    ((2018, 5, 22), [c.TEMPORA_PASC7_2], []),
    ((2018, 5, 23), [c.TEMPORA_PASC7_3], []),
    ((2018, 5, 24), [c.TEMPORA_PASC7_4], []),
    ((2018, 5, 25), [c.TEMPORA_PASC7_5], []),
    ((2018, 5, 26), [c.TEMPORA_PASC7_6], []),
    ((2018, 5, 27), [c.TEMPORA_PENT01_0], []),  # Trinity Sunday, no comm.
    ((2018, 5, 31), [c.TEMPORA_PENT01_4], []),  # Corpus Christi, no comm.
    ((2018, 6, 10), [c.TEMPORA_PENT03_0], []),  # Sunday, no low class comm.
    ((2018, 10, 28), [c.SANCTI_10_DUr], []),  # Feast of Christ the King; no comm
    ((2018, 11, 14), [c.SANCTI_11_14], []),
    ((2018, 11, 26), [c.SANCTI_11_26], []),
    ((2018, 12, 5), [c.TEMPORA_ADV1_3], [c.SANCTI_12_05]),
    ((2018, 12, 10), [c.TEMPORA_ADV2_1], [c.SANCTI_12_10]),
    # Sanctae Mariae Sabbato
    ((2019, 1, 5), [c.C_10B], []),
    ((2019, 1, 12), [c.C_10B], []),
    ((2019, 1, 19), [c.C_10B], [c.SANCTI_01_19]),
    ((2019, 2, 16), [c.C_10C], []),
    ((2015, 2, 14), [c.C_10C], [c.SANCTI_02_14]),
    ((2019, 7, 6), [c.C_10T], []),
    ((2019, 7, 27), [c.C_10T], [c.SANCTI_07_27]),
    ((2016, 4, 23), [c.C_10PASC], [c.SANCTI_04_23]),
    ((2017, 5, 6), [c.C_10PASC], []),
])
def test_given_date_contains_proper_day_ids(date_, celebration, commemoration):
    assert [i.id for i in get_missal(date_[0])[date(*date_)].celebration] == celebration
    assert [i.id for i in get_missal(date_[0])[date(*date_)].commemoration] == commemoration


@pytest.mark.parametrize("date_,not_expected_day_ids", [
    ((2018, 12, 24), [c.PATTERN_ADVENT]),
    ((2018, 12, 25), [c.PATTERN_ADVENT]),
    ((2018, 12, 26), [c.PATTERN_ADVENT]),
    ((2018, 1, 14), [c.SANCTI_01_14]),
    ((2018, 1, 21), [c.SANCTI_01_21]),
    ((2018, 1, 21), [c.SANCTI_01_21]),
    ((2018, 11, 25), [c.SANCTI_11_25]),
    ((2016, 2, 28), [c.SANCTI_02_27]),  # leap year
])
def test_given_date_does_not_contain_day_ids(date_, not_expected_day_ids):
    assert not match(get_missal(date_[0])[date(*date_)].all, not_expected_day_ids)


@pytest.mark.parametrize("date_,expected_celebration,expected_commemoration", [
    # occurence of 2nd class sunday and 2nd class feast
    ((1996, 9, 8), [c.TEMPORA_PENT15_0], [c.SANCTI_09_08]),
    ((2009, 7, 26), [c.TEMPORA_PENT08_0], [c.SANCTI_07_26]),
    ((2019, 9, 15), [c.TEMPORA_PENT14_0], [c.SANCTI_09_15]),
    ((2018, 10, 7), [c.TEMPORA_PENT20_0], [c.SANCTI_10_07]),
    # ash wednesday and weeks of holy week always win
    ((2008, 2, 6), [c.TEMPORA_QUADP3_3], []),
    ((2011, 3, 9), [c.TEMPORA_QUADP3_3], []),
    ((2012, 2, 22), [c.TEMPORA_QUADP3_3], []),
    ((2015, 2, 18), [c.TEMPORA_QUADP3_3], []),
    ((2044, 4, 11), [c.TEMPORA_QUAD6_1], []),
    ((2018, 3, 27), [c.TEMPORA_QUAD6_2], []),
    ((2044, 4, 13), [c.TEMPORA_QUAD6_3], []),
    ((2044, 4, 14), [c.TEMPORA_QUAD6_4], []),
    ((1952, 4, 11), [c.TEMPORA_QUAD6_5], []),
    ((1954, 4, 17), [c.TEMPORA_QUAD6_6], []),
    ((1960, 4, 17), [c.TEMPORA_PASC0_0], []),
    # advent feria 17-24, ember days of lent, september and advent give away to 2nd class feast
    ((2018, 2, 24), [c.SANCTI_02_24], [c.TEMPORA_QUAD1_6]),
    ((1972, 2, 25), [c.SANCTI_02_24], [c.TEMPORA_QUAD1_5]),
    ((2019, 9, 21), [c.SANCTI_09_21], [c.TEMPORA_PENT_6]),
    ((2018, 12, 21), [c.SANCTI_12_21], [c.TEMPORA_ADV3_5]),
])
def test_conflicts(date_, expected_celebration, expected_commemoration):
    missal = get_missal(date_[0])
    assert [i.id for i in missal[date(*date_)].celebration] == expected_celebration
    assert [i.id for i in missal[date(*date_)].commemoration] == expected_commemoration


@pytest.mark.parametrize("day_id,date_,expected_weekday", [
    (c.TEMPORA_EPI2_3, (2002, 1, 23), 2),
    (c.TEMPORA_QUADP1_0, (2002, 1, 27), 6),
    (c.TEMPORA_QUADP1_0, (2002, 1, 28), 6)
])
def test_liturgical_days_fall_in_proper_weedays(day_id, date_, expected_weekday):
    assert LiturgicalDay(day_id, date(*date_)).weekday == expected_weekday


@pytest.mark.parametrize("day_id,date_,expected_rank", [
    # Days with unchanged ranks
    (c.TEMPORA_EPI2_3, (2002, 1, 23), 4),
    (c.TEMPORA_QUADP1_0, (2002, 1, 27), 2),
    # Advent 2002 - increased ranks of feria days from Dec 17
    (c.TEMPORA_ADV3_1, (2002, 12, 16), 3),
    (c.TEMPORA_ADV3_2, (2002, 12, 17), 2),
    (c.TEMPORA_ADV3_3, (2002, 12, 18), 2),
    (c.TEMPORA_ADV3_4, (2002, 12, 19), 2),
    (c.TEMPORA_ADV3_5, (2002, 12, 20), 2),
    (c.TEMPORA_ADV3_6, (2002, 12, 21), 2),
    (c.TEMPORA_ADV4_0, (2002, 12, 22), 1),
    (c.TEMPORA_ADV4_1, (2002, 12, 23), 2),
    # Advent 2015 - increased ranks of feria days from Dec 17
    (c.TEMPORA_ADV3_2, (2015, 12, 15), 3),
    (c.TEMPORA_ADV3_3, (2015, 12, 16), 2),
    (c.TEMPORA_ADV3_4, (2015, 12, 17), 2),
    (c.TEMPORA_ADV3_5, (2015, 12, 18), 2),
    (c.TEMPORA_ADV3_6, (2015, 12, 19), 2),
    (c.TEMPORA_ADV4_0, (2015, 12, 20), 1),
    (c.TEMPORA_ADV4_1, (2015, 12, 21), 2),
    (c.TEMPORA_ADV4_2, (2015, 12, 22), 2),
    (c.TEMPORA_ADV4_3, (2015, 12, 23), 2)
])
def test_liturgical_days_have_proper_ranks(day_id, date_, expected_rank):
    assert LiturgicalDay(day_id, date(*date_)).rank == expected_rank


def test_liturgical_day_compare():
    rank_1_1 = LiturgicalDay(c.TEMPORA_PASC7_0, date(2015, 5, 24))
    rank_1_2 = LiturgicalDay(c.SANCTI_11_01, date(2015, 11, 1))
    rank_2_1 = LiturgicalDay(c.TEMPORA_EPI1_0, date(2015, 1, 11))
    rank_2_2 = LiturgicalDay(c.SANCTI_01_13, date(2015, 1, 13))
    rank_3_1 = LiturgicalDay(c.TEMPORA_QUAD5_5, date(2015, 3, 27))
    rank_3_2 = LiturgicalDay(c.SANCTI_03_28, date(2015, 3, 28))
    rank_4_1 = LiturgicalDay(c.TEMPORA_PENT01_1, date(2015, 6, 1))
    rank_4_2 = LiturgicalDay(c.SANCTI_08_09, date(2015, 8, 9))

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
