import datetime
import json
import pytest
from datetime import date

from api.constants.common import *
from backend.tests.test_propers import _tests_propers
from .util import update_propers_for_dates

from .conftest import get_missal, HERE

years = [
    '2024',
    '2025',
]

days = [    
    '01-01',
    '01-02',
    '01-03',
    '01-04',
    '01-05',
    '01-06',
    '01-07',
    '01-08',
    '01-09',
    '01-10',
    ]


def _get_proper_fixtures(fixture):
    dates = [f"{y}-{d}" for y in years for d in days]
    with open(os.path.join(HERE, 'fixtures/{}'.format(fixture))) as fh:
        x = json.load(fh)
        # return [i for i in x.items() if i[0][5:] >= '01-01' and i[0][5:] <= '12-31']
        # return [i for i in x.items() if i[0][5:] >= '09-01' and i[0][5:] <= '09-20']
        return [i for i in x.items() if i[0] in dates]

@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures(f"propers_{LANGUAGE_LATIN}.json"))
def test_all_propers_latin(strdate, expected_sections):
    _tests_propers(LANGUAGE_LATIN, strdate=strdate, expected_sections=expected_sections)


@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures(f"propers_{LANGUAGE_POLSKI}.json"))
def test_all_propers_polish(strdate, expected_sections):
    _tests_propers(LANGUAGE_POLSKI, strdate=strdate, expected_sections=expected_sections)


@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures(f"propers_{LANGUAGE_ENGLISH}.json"))
def test_all_propers_english(strdate, expected_sections):
    _tests_propers(LANGUAGE_ENGLISH, strdate=strdate, expected_sections=expected_sections)


@pytest.mark.skip
@pytest.mark.parametrize("language", [
    # 'la',
    # 'pl',
    'en'
    ])
def test_update_fixtures(language):
    dates_strs = [f"{y}-{d}" for y in years for d in days]
    datetimes = [datetime.date(*[int(j) for j in i.split('-')]) for i in dates_strs]
    update_propers_for_dates(
        datetimes,
        language,
        os.path.join(HERE, "fixtures", f"propers_{language}.json")
    )