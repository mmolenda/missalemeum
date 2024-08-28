import os

import pytest
from unittest.mock import patch

from propers.models import Proper
from propers.parser import ProperParser
language = 'en'

HERE = os.path.abspath(os.path.dirname(__file__))


def print_proper(proper: Proper):
    print(f"\n#### {proper.lang.upper()}")
    for k, v in proper.items():
        print(f"# {v}")


@patch("propers.parser.cc")
@pytest.mark.parametrize("id_,sections_lat,sections_vern", [
    ("sancti:11-11:3:w", {"Introitus": "LA 11-11 Introit", "Oratio": "LA C4a Oratio"}, {"Introitus": "EN 11-11 Introit", "Oratio": "EN C4a Oratio"}),
    ("sancti:11-12:3:r", {"Introitus": "LA 11-12 Introit", "Oratio": "LA C4 Oratio"}, {"Introitus": "EN 11-12 Introit", "Oratio": "EN C4 Oratio"}),
    ("sancti:11-14:3:w", {"Introitus": "LA 11-14 Introit", "Oratio": "LA C4 Oratio"}, {"Introitus": "EN 11-14 Introit", "Oratio": "EN C4 Oratio"}),
    ("sancti:07-08:3:w", {"Introitus": "LA C7a Introitus", "Oratio": "LA 07-08 Oratio", "Secreta": "LA C6b Secreta"},
                         {"Introitus": "EN C7a Introitus", "Oratio": "EN 07-08 Oratio", "Secreta": "EN C6b Secreta"}),
])
def test_parser1(constants_common, id_: str, sections_lat: dict, sections_vern: dict):
    parser = ProperParser(id_, language)
    constants_common.CUSTOM_DIVOFF_DIR = os.path.join(HERE, "fixtures", "divinum-officium")
    proper_vern, proper_lat = parser.parse()

    print_proper(proper_lat)
    print_proper(proper_vern)

    assert proper_lat.id == id_
    for section_name, section_content in sections_lat.items():
        assert proper_lat.get_section(section_name).body[0] == section_content
    assert proper_vern.id == id_
    for section_name, section_content in sections_vern.items():
        assert proper_vern.get_section(section_name).body[0] == section_content
