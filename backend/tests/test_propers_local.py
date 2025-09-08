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
    "07-02",
    # "07-06",
    # "07-07",
    # "07-08",
    # "07-11",
    # "07-12",
    # "07-13",
    # "07-14",
    # "07-15",
    # "07-18",
    # "07-19",
    # "07-20",
    # "07-21",
    # "07-22",
    # "07-23",
    # "07-24",
    # "07-25",
    # "07-26",
    # "07-27",
    # "07-29",
    # "07-31",
]


def _get_proper_fixtures(fixture):
    dates = [f"{y}-{d}" for y in years for d in days]
    with open(os.path.join(HERE, "fixtures/{}".format(fixture))) as fh:
        x = json.load(fh)
        # return [i for i in x.items() if i[0][5:] >= "07-01" and i[0][5:] <= "07-31"]
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
