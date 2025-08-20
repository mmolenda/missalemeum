import json
import pytest
from datetime import date

from api.constants.common import *

from .conftest import get_missal, HERE

language = 'pl'



def _get_proper_fixtures(fixture):

    # in custom:
    # 01-25

    years = [
        '2024',
        '2025',
    ]
    days = [
        '02-17'
    ]
    dates = [f"{y}-{d}" for y in years for d in days]
    with open(os.path.join(HERE, 'fixtures/{}'.format(fixture))) as fh:
        x = json.load(fh)
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
    _, proper = day.get_proper()[0]
    proper_serialized = proper.serialize()
    for i, expected_section in enumerate(expected_sections):
        assert expected_section['id'] == proper_serialized[i]['id'],\
            f'latin {tempora_name or proper.title}/{strdate}/{expected_section["id"]}'
        assert expected_section['body'] in proper_serialized[i]['body'],\
            f'latin {tempora_name or proper.title}/{strdate}/{expected_section["id"]}'


@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures("propers_pl.json"))
def test_all_propers_polish(strdate, expected_sections):
    strdate_bits = [int(i) for i in strdate.split('-')]
    missal = get_missal(strdate_bits[0], 'pl')
    day = missal.get_day(date(*strdate_bits))
    tempora_name = day.get_tempora_name()
    proper, _ = day.get_proper()[0]
    proper_serialized = proper.serialize()
    for i, expected_section in enumerate(expected_sections):
        assert expected_section['id'] == proper_serialized[i]['id'],\
            f'polish {tempora_name or proper.title}/{strdate}/{expected_section["id"]}'
        assert expected_section['body'] in proper_serialized[i]['body'],\
            f'polish {tempora_name or proper.title}/{strdate}/{expected_section["id"]}'


@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures("propers_en.json"))
def test_all_propers_english(strdate, expected_sections):
    strdate_bits = [int(i) for i in strdate.split('-')]
    missal = get_missal(strdate_bits[0], 'en')
    day = missal.get_day(date(*strdate_bits))
    tempora_name = day.get_tempora_name()
    proper, _ = day.get_proper()[0]
    proper_serialized = proper.serialize()
    for i, expected_section in enumerate(expected_sections):
        assert expected_section['id'] == proper_serialized[i]['id'], \
            f'english {tempora_name or proper.title}/{strdate}/{expected_section["id"]}'
        assert expected_section['body'] in proper_serialized[i]['body'], \
            f'english {tempora_name or proper.title}/{strdate}/{expected_section["id"]}'
