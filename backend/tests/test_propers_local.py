import datetime
import json
import pytest
from datetime import date

from api.constants.common import *
from .util import update_propers_for_dates

from .conftest import get_missal, HERE

languages = [
    'pl',
    # 'en',
    # 'la'
    ]
years = [
    '2024',
    '2025',
]
days = [
    '03-14',
    ]


def _get_proper_fixtures(fixture):
    dates = [f"{y}-{d}" for y in years for d in days]
    with open(os.path.join(HERE, 'fixtures/{}'.format(fixture))) as fh:
        x = json.load(fh)
        # return [i for i in x.items() if i[0][5:] >= '01-01' and i[0][5:] <= '03-11']
        return [i for i in x.items() if i[0] in dates]

@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures("propers_la.json"))
def test_all_propers_latin(strdate, expected_sections):
    """
    We test propers for two years (one with early Easter and one with late Easter) to make sure most
    of the variants are covered. For example in one year there's a Sunday on certain day which supersede
    saint's feast, so we want to test this day from the other year to make sure that the latter feast
    is covered as well.
    """
    strdate_bits = [int(i) for i in strdate.split('-')]
    missal = get_missal(strdate_bits[0], 'pl')
    day = missal.get_day(date(*strdate_bits))
    tempora_name = day.get_tempora_name()
    propers = day.get_proper()
    for j, propers in enumerate(day.get_proper()):
        _, proper = propers
        proper_serialized = proper.serialize()
        for i, expected_section in enumerate(expected_sections[j]):
            assert expected_section['id'] == proper_serialized[i]['id'],\
                f'latin/{j}/{tempora_name or proper.title}/{strdate}/{expected_section["id"]}'
            assert expected_section['body'] in proper_serialized[i]['body'],\
                f'latin/{j}/{tempora_name or proper.title}/{strdate}/{expected_section["id"]}'


@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures("propers_pl.json"))
def test_all_propers_polish(strdate, expected_sections):
    strdate_bits = [int(i) for i in strdate.split('-')]
    missal = get_missal(strdate_bits[0], 'pl')
    day = missal.get_day(date(*strdate_bits))
    tempora_name = day.get_tempora_name()
    propers = day.get_proper()
    for j, propers in enumerate(day.get_proper()):
        proper, _ = propers
        proper_serialized = proper.serialize()
        for i, expected_section in enumerate(expected_sections[j]):
            assert expected_section['id'] == proper_serialized[i]['id'],\
                f'polish/{j}/{tempora_name or proper.title}/{strdate}/{expected_section["id"]}'
            assert expected_section['body'] in proper_serialized[i]['body'],\
                f'polish/{j}/{tempora_name or proper.title}/{strdate}/{expected_section["id"]}'


@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures("propers_en.json"))
def test_all_propers_english(strdate, expected_sections):
    strdate_bits = [int(i) for i in strdate.split('-')]
    missal = get_missal(strdate_bits[0], 'en')
    day = missal.get_day(date(*strdate_bits))
    tempora_name = day.get_tempora_name()
    propers = day.get_proper()
    for j, propers in enumerate(day.get_proper()):
        proper, _ = propers
        proper_serialized = proper.serialize()
        for i, expected_section in enumerate(expected_sections[j]):
            assert expected_section['id'] == proper_serialized[i]['id'], \
                f'english/{j}/{tempora_name or proper.title}/{strdate}/{expected_section["id"]}'
            assert expected_section['body'] in proper_serialized[i]['body'], \
                f'english/{j}/{tempora_name or proper.title}/{strdate}/{expected_section["id"]}'


@pytest.mark.skip
def test_update_fixtures():
    for language in languages:
        dates_strs = [f"{y}-{d}" for y in years for d in days]
        datetimes = [datetime.date(*[int(j) for j in i.split('-')]) for i in dates_strs]
        update_propers_for_dates(
            datetimes,
            language,
            os.path.join(HERE, "fixtures", f"propers_{language}.json")
        )