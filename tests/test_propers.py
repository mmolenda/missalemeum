from datetime import date
from exceptions import InvalidInput, ProperNotFound

import pytest

from constants import common as c
from kalendar.models import Observance
from propers.parser import ProperParser
from tests.conftest import get_missal

language = 'Polski'


def test_parse_proper_no_refs():
    proper_vernacular, proper_latin = ProperParser.parse(c.SANCTI_01_06, language)

    assert 'Objawienie' in proper_vernacular.get_section('Comment').body[0]
    assert 'Ml 3:1' in proper_vernacular.get_section('Introitus').body[0]
    assert 'Boże, w dniu dzisiejszym' in proper_vernacular.get_section('Oratio').body[0]
    assert '*Iz 60:1-6*' in proper_vernacular.get_section('Lectio').body[1]
    assert 'Iz 60:6; 60:1' in proper_vernacular.get_section('Graduale').body[0]
    assert '*Mt 2:1-12*' in proper_vernacular.get_section('Evangelium').body[1]
    assert 'Ps 71:10-11' in proper_vernacular.get_section('Offertorium').body[0]
    assert 'Wejrzyj miłościwie' in proper_vernacular.get_section('Secreta').body[0]
    assert 'Mt 2:2' in proper_vernacular.get_section('Communio').body[0]
    assert 'Spraw, prosimy,' in proper_vernacular.get_section('Postcommunio').body[0]
    assert 'Prefacja o Objawieniu' in proper_vernacular.get_section('Prefatio').body[0]

    assert 'Malach 3:1' in proper_latin.get_section('Introitus').body[0]
    assert 'Deus, qui hodiérna die' in proper_latin.get_section('Oratio').body[0]
    assert '*Is 60:1-6*' in proper_latin.get_section('Lectio').body[1]
    assert '*Isa 60:6; 60:1*' in proper_latin.get_section('Graduale').body[0]
    assert '*Matt 2:1-12*' in proper_latin.get_section('Evangelium').body[1]
    assert '*Ps 71:10-11*' in proper_latin.get_section('Offertorium').body[0]
    assert 'Ecclésiæ tuæ, quǽsumus' in proper_latin.get_section('Secreta').body[0]
    assert '*Matt 2:2*' in proper_latin.get_section('Communio').body[0]
    assert 'Præsta, quǽsumus, omnípotens' in proper_latin.get_section('Postcommunio').body[0]
    assert '*de Epiphania Domini*' in proper_latin.get_section('Prefatio').body[0]


def test_parse_proper_refs_inside_sections_and_in_vide():
    proper_vernacular, proper_latin = ProperParser.parse(c.SANCTI_01_22, language)

    assert '## 22 I – Śś. Wincentego' in proper_vernacular.get_section('Comment').body[0]
    assert '*Ps 78:11-12; 78:10*' in proper_vernacular.get_section('Introitus').body[0]
    assert 'Przychyl się, Panie,' in proper_vernacular.get_section('Oratio').body[0]
    assert '*Mdr 3:1-8*' in proper_vernacular.get_section('Lectio').body[1]
    assert '*Wj 15:11*' in proper_vernacular.get_section('Graduale').body[0]
    assert '*Wj 15:11*' in proper_vernacular.get_section('Tractus').body[0]
    assert '*Łk 21:9-19*' in proper_vernacular.get_section('Evangelium').body[1]
    assert '*Ps 67:36*' in proper_vernacular.get_section('Offertorium').body[0]
    assert 'Ofiarujemy Ci, Panie, te dary' in proper_vernacular.get_section('Secreta').body[0]
    assert '*Mdr 3:4-6*' in proper_vernacular.get_section('Communio').body[0]
    assert 'Prosimy Cię, wszechmogący' in proper_vernacular.get_section('Postcommunio').body[0]
    assert 'Prefacja zwykła' in proper_vernacular.get_section('Prefatio').body[0]

    assert '*Ps 78:11-12; 78:10*' in proper_latin.get_section('Introitus').body[0]
    assert 'Adésto, Dómine, supplicatiónibus' in proper_latin.get_section('Oratio').body[0]
    assert '*Sap 3:1-8*' in proper_latin.get_section('Lectio').body[1]
    assert '*Exod 15:11*' in proper_latin.get_section('Graduale').body[0]
    assert '*Exod 15:11*' in proper_latin.get_section('Tractus').body[0]
    assert '*Luc 21:9-19*' in proper_latin.get_section('Evangelium').body[1]
    assert '*Ps 67:36*' in proper_latin.get_section('Offertorium').body[0]
    assert 'Múnera tibi, Dómine,' in proper_latin.get_section('Secreta').body[0]
    assert '*Sap 3:4-6*' in proper_latin.get_section('Communio').body[0]
    assert 'Quǽsumus, omnípotens Deus:' in proper_latin.get_section('Postcommunio').body[0]
    assert '*Communis*' in proper_latin.get_section('Prefatio').body[0]


def test_parse_proper_ref_outside_sections():
    proper_vernacular, proper_latin = ProperParser.parse(c.SANCTI_10_DUr, language)
    assert '## Chrystusa Króla' in proper_vernacular.get_section('Comment').body[0]
    assert '*Ap 5:12; 1:6*' in proper_vernacular.get_section('Introitus').body[0]
    assert '*Apoc 5:12; 1:6*' in proper_latin.get_section('Introitus').body[0]


def test_invalid_proper_id():
    with pytest.raises(InvalidInput):
        ProperParser.parse('bla', language)


def test_proper_not_found():
    with pytest.raises(ProperNotFound):
        ProperParser.parse('tempora:bla', language)


def test_get_proper_from_observance():
    proper_vernacular, proper_latin = Observance(c.SANCTI_01_06, date(2018, 1, 6), language).get_proper()
    assert 'Objawienie' in proper_vernacular.get_section('Comment').body[0]
    assert 'Ml 3:1' in proper_vernacular.get_section('Introitus').body[0]
    assert 'Malach 3:1' in proper_latin.get_section('Introitus').body[0]
    assert 'Deus, qui hodiérna die' in proper_latin.get_section('Oratio').body[0]


def test_get_proper_from_day():
    missal = get_missal(2018, language)
    proper_vernacular, proper_latin = missal.get_day(date(2018, 1, 6)).get_proper()[0]
    assert 'Objawienie' in proper_vernacular.get_section('Comment').body[0]
    assert 'Ml 3:1' in proper_vernacular.get_section('Introitus').body[0]
    assert 'Malach 3:1' in proper_latin.get_section('Introitus').body[0]
    assert 'Deus, qui hodiérna die' in proper_latin.get_section('Oratio').body[0]


@pytest.mark.parametrize("date_,proper", [
    ((2018, 1, 4), 'In Circumcisione Domini'),
    ((2018, 1, 12), 'Dominica infra Octavam Epiphaniae'),  # Feast of the Holy Family
    ((2018, 2, 13), 'Dominica in Quinquagesima'),
    ((2018, 7, 4), 'Dominica VI Post Pentecosten'),
    ((2018, 7, 9), 'Dominica VII Post Pentecosten'),  # Feast of the Most Precious Blood
    ((2018, 10, 31), 'Dominica XXIII Post Pentecosten'),  # Feast of Christ the King
])
def test_get_proper_for_day_without_own_proper(date_, proper):
    # For days without their own propers we show the proper from the last Sunday
    missal = get_missal(date_[0], language)
    _, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    assert proper in proper_latin.get_section('Rank').body[0]


def test_get_repr():
    missal = get_missal(2018, language)
    container = missal.get_day(date(2018, 1, 13))
    assert 'Sobota po 1 Niedzieli po Objawieniu' in container.get_tempora_name()
    assert 'Wspomnienie Chrztu Pańskiego' in container.get_celebration_name()
    assert str(container) == '[<tempora:Epi1-6:4>][<sancti:01-13:2>][]'


@pytest.mark.parametrize("date_,sections", [
    ((2018, 12, 11), ['Commemoratio Oratio', 'Commemoratio Secreta', 'Commemoratio Postcommunio']),
    ((2018, 12, 7), ['Commemoratio Oratio', 'Commemoratio Secreta', 'Commemoratio Postcommunio']),
    ((2018, 12, 6), ['Rank1570'])
])
def test_ignored_sections(date_, sections):
    missal = get_missal(date_[0], language)
    _, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    for section in sections:
        assert proper_latin.get_section(section) is None
