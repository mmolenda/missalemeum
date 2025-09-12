import json
import pytest

from api.constants.common import *
from .test_propers import _tests_propers

from .conftest import get_missal, HERE

# 2024-03-27 W. Środa dicuntur ommituntur etc.
# 2025-04-15 W. Wtorek dicuntur ommituntur etc.
# 2025-04-16 W. Sroda dicuntur ommituntur etc.

years = [
    "2024",
    "2025",
]

days = [
    "12-05",
    # "12-07",
    # "12-10",
    # "12-11",
    # "12-13",
    # "12-16",
    # "12-17",
    # "12-18",
    # "12-19",
    # "12-20",
    # "12-25",
    # "12-29",
    # "12-30",
    # "12-31",
]


def _get_proper_fixtures(fixture):
    dates = [f"{y}-{d}" for y in years for d in days]
    with open(os.path.join(HERE, "fixtures/{}".format(fixture))) as fh:
        x = json.load(fh)
        # return [i for i in x.items() if i[0][5:] >= "12-01" and i[0][5:] <= "12-31"]
        return [i for i in x.items() if i[0] in dates]


@pytest.mark.parametrize(
    "strdate,expected_sections", _get_proper_fixtures(f"propers_{LANGUAGE_LATIN}.json")
)
def test_all_propers_latin(strdate, expected_sections):
    _tests_propers(LANGUAGE_LATIN, strdate=strdate, expected_sections=expected_sections)


@pytest.mark.parametrize(
    "strdate,expected_sections", _get_proper_fixtures(f"propers_{LANGUAGE_POLSKI}.json")
)
def test_all_propers_polish(strdate, expected_sections):
    _tests_propers(
        LANGUAGE_POLSKI, strdate=strdate, expected_sections=expected_sections
    )


@pytest.mark.parametrize(
    "strdate,expected_sections",
    _get_proper_fixtures(f"propers_{LANGUAGE_ENGLISH}.json"),
)
def test_all_propers_english(strdate, expected_sections):
    _tests_propers(
        LANGUAGE_ENGLISH, strdate=strdate, expected_sections=expected_sections
    )
