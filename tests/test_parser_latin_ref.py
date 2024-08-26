import os

import pytest
from unittest.mock import patch

from propers.models import Proper
from propers.parser_latin_ref import ProperParserLatinRef
language = 'en'

HERE = os.path.abspath(os.path.dirname(__file__))


def print_proper(proper: Proper):
    print(f"\n#### {proper.lang.upper()}")
    for k, v in proper.items():
        print(f"# {v}")


@patch("propers.parser.cc")
@pytest.mark.parametrize("id_,introit_lat,oratio_lat,introit_vern,oratio_vern", [
    ("sancti:11-11:3:w", "LA 11-11 Introit", "LA C4a Oratio", "EN 11-11 Introit", "EN C4a Oratio"),
    ("sancti:11-12:3:r", "LA 11-12 Introit", "LA C4 Oratio", "EN 11-12 Introit", "EN C4 Oratio"),
    ("sancti:11-14:3:w", "LA 11-14 Introit", "LA C4 Oratio", "EN 11-14 Introit", "EN C4 Oratio"),
])
def test_parser1(constants_common, id_: str, introit_lat: str, oratio_lat, introit_vern, oratio_vern):
    parser = ProperParserLatinRef(id_, language)
    constants_common.CUSTOM_DIVOFF_DIR = os.path.join(HERE, "fixtures", "divinum-officium")
    proper_vern, proper_lat = parser.parse()
    assert proper_lat.id == id_
    assert proper_lat.get_section("Introitus").body[0] == introit_lat
    assert proper_lat.get_section("Oratio").body[0] == oratio_lat
    assert proper_vern.id == id_
    # assert proper_vern.get_section("Introitus").body[0] == introit_vern
    # assert proper_vern.get_section("Oratio").body[0] == oratio_vern

    print_proper(proper_lat)
    print_proper(proper_vern)


