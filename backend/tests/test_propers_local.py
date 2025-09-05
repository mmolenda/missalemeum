import json
import pytest

from api.constants.common import *
from .test_propers import _tests_propers

from .conftest import get_missal, HERE

years = [
    '2024',
    '2025',
]

days = [
    '01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07', '01-08', '01-09', '01-10',
    '01-11', '01-12', '01-13', '01-14', '01-15', '01-16', '01-17', '01-18', '01-19', '01-20',
    '01-21', '01-22', '01-23', '01-24', '01-25', '01-26', '01-27', '01-28', '01-29', '01-30',
    '01-31',
    '02-01', '02-02', '02-03', '02-04', '02-05', '02-06', '02-07', '02-08', '02-09', '02-10',
    '02-11', '02-12', '02-13', '02-14', '02-15', '02-16', '02-17', '02-18', '02-19', '02-20',
    '02-21', '02-22', '02-23', '02-24', '02-25', '02-26', '02-27', '02-28'
]


def _get_proper_fixtures(fixture):
    dates = [f"{y}-{d}" for y in years for d in days]
    with open(os.path.join(HERE, 'fixtures/{}'.format(fixture))) as fh:
        x = json.load(fh)
        return [i for i in x.items() if i[0][5:] >= '01-01' and i[0][5:] <= '02-29']
        # return [i for i in x.items() if i[0][5:] >= '09-01' and i[0][5:] <= '09-20']
        # return [i for i in x.items() if i[0] in dates]

@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures(f"propers_{LANGUAGE_LATIN}.json"))
def test_all_propers_latin(strdate, expected_sections):
    _tests_propers(LANGUAGE_LATIN, strdate=strdate, expected_sections=expected_sections)


@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures(f"propers_{LANGUAGE_POLSKI}.json"))
def test_all_propers_polish(strdate, expected_sections):
    _tests_propers(LANGUAGE_POLSKI, strdate=strdate, expected_sections=expected_sections)


@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures(f"propers_{LANGUAGE_ENGLISH}.json"))
def test_all_propers_english(strdate, expected_sections):
    _tests_propers(LANGUAGE_ENGLISH, strdate=strdate, expected_sections=expected_sections)
