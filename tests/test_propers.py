from datetime import date
from exceptions import InvalidInput, ProperNotFound

import pytest

from constants import common as c
from kalendar.models import Observance
from propers.models import ProperConfig
from propers.parser import ProperParser
from tests.conftest import get_missal

language = 'Polski'


def test_parse_proper_no_refs():
    proper_vernacular, proper_latin = ProperParser(c.SANCTI_01_06, language).parse()

    assert 'Objawienie' in proper_vernacular.title
    assert 1 == proper_vernacular.rank
    assert '«Obchodzimy dzień święty' in proper_vernacular.description
    assert 'Stacja u Św. Piotra' in proper_vernacular.additional_info
    assert 'Szaty białe' in proper_vernacular.additional_info
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
    proper_vernacular, proper_latin = ProperParser(c.SANCTI_01_22, language).parse()

    assert 'Śś. Wincentego' in proper_vernacular.title
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
    proper_vernacular, proper_latin = ProperParser(c.SANCTI_10_DUr, language).parse()
    assert 'Chrystusa Króla' in proper_vernacular.title
    assert '*Ap 5:12; 1:6*' in proper_vernacular.get_section('Introitus').body[0]
    assert '*Apoc 5:12; 1:6*' in proper_latin.get_section('Introitus').body[0]


def test_invalid_proper_id():
    with pytest.raises(InvalidInput):
        ProperParser('bla', language).parse()


def test_proper_not_found():
    with pytest.raises(ProperNotFound):
        ProperParser('tempora:bla', language).parse()


def test_get_proper_from_observance():
    proper_vernacular, proper_latin = Observance(c.SANCTI_01_06, date(2018, 1, 6), language).get_proper()
    assert 'Objawienie' in proper_vernacular.title
    assert 'Ml 3:1' in proper_vernacular.get_section('Introitus').body[0]
    assert 'Malach 3:1' in proper_latin.get_section('Introitus').body[0]
    assert 'Deus, qui hodiérna die' in proper_latin.get_section('Oratio').body[0]


def test_get_proper_from_day():
    missal = get_missal(2018, language)
    proper_vernacular, proper_latin = missal.get_day(date(2018, 1, 6)).get_proper()[0]
    assert 'Objawienie' in proper_vernacular.title
    assert 'Ml 3:1' in proper_vernacular.get_section('Introitus').body[0]
    assert 'Malach 3:1' in proper_latin.get_section('Introitus').body[0]
    assert 'Deus, qui hodiérna die' in proper_latin.get_section('Oratio').body[0]


@pytest.mark.parametrize("date_,id_,rank", [
    ((2018, 1, 4), 'sancti:01-01:1', 4),
    ((2018, 1, 12), 'tempora:Epi1-0a:2', 4),  # Feast of the Holy Family
    ((2018, 2, 13), 'tempora:Quadp3-0:2', 4),
    ((2018, 7, 4), 'tempora:Pent06-0:2', 4),
    ((2018, 7, 9), 'tempora:Pent07-0:2', 4),  # Feast of the Most Precious Blood
    ((2018, 10, 31), 'tempora:Pent23-0:2', 4),  # Feast of Christ the King
])
def test_get_proper_for_day_without_own_proper(date_, id_, rank):
    # For days without their own propers we show the proper from the last Sunday
    missal = get_missal(date_[0], language)
    _, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    assert proper_latin.id == id_
    assert proper_latin.rank == rank


def test_get_repr():
    missal = get_missal(2018, language)
    container = missal.get_day(date(2018, 1, 13))
    assert 'Sobota po 1 Niedzieli po Objawieniu' in container.get_tempora_name()
    assert 'Wspomnienie Chrztu Pańskiego' in container.get_celebration_name()
    assert str(container) == '[<tempora:Epi1-6:4>][<sancti:01-13:2>][]'


@pytest.mark.parametrize("date_,sections", [
    ((2018, 12, 11), ['Commemoratio Oratio', 'Commemoratio Secreta', 'Commemoratio Postcommunio']),
    ((2018, 12, 7), ['Commemoratio Oratio', 'Commemoratio Secreta', 'Commemoratio Postcommunio']),
    ((2018, 12, 6), ['Rank1570']),
    ((2019, 3, 25), ['Graduale'])
])
def test_ignored_sections(date_, sections):
    missal = get_missal(date_[0], language)
    _, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    for section in sections:
        assert proper_latin.get_section(section) is None


@pytest.mark.parametrize("date_,title_part,preface_body", [
    ((2018, 10, 28), 'Chrystusa Króla', '*de D.N. Jesu Christi Rege*'),
    ((2018, 12, 16), '3 Niedziela Adwentu', '*de sanctissima Trinitate*'),
    ((2018, 12, 17), '3 Niedziela Adwentu', '*Communis*'),
    ((2019, 6, 24), 'Narodzenie Św. Jana Chrzciciela', '*Communis*'),
    ((2019, 4, 27), 'Sobota Biała', '*Paschalis*'),
    ((2019, 4, 30), 'Katarzyny Sieneńskiej', '*Paschalis*'),
    ((2019, 5, 1), 'Józefa Robotnika', '*de S. Joseph*'),
    ((2019, 1, 25), 'Nawrócenie św. Pawła, Apostoła', '*de Apostolis*'),
    ((2019, 7, 25), 'Św. Jakuba, Apostoła', '*de Apostolis*'),
    ((2019, 12, 21), 'Św. Tomasza, Apostoła', '*de Apostolis*'),
])
def test_correct_preface_calculated_by_date(date_,title_part, preface_body):
    missal = get_missal(date_[0], language)
    proper_vernacular, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    assert title_part in proper_vernacular.title
    assert preface_body == proper_latin.get_section('Prefatio').get_body()[0]


@pytest.mark.parametrize("proper_id,preface_name,preface_body", [
    ('tempora:Adv2-0', 'Communis', '*Communis*'),
    ('tempora:Adv2-0', 'Trinitate', '*de sanctissima Trinitate*'),
])
def test_correct_preface_calculated_by_proper_id(proper_id, preface_name, preface_body):
    _, proper_latin = ProperParser(proper_id, language, ProperConfig(preface=preface_name)).parse()
    assert preface_body == proper_latin.get_section('Prefatio').get_body()[0]


@pytest.mark.parametrize("date_,title_part,sections_present,sections_absent", [
    ((2019, 7, 3), 'Ireneusza', ('Graduale', ), ('GradualeP', 'Tractus')),
    ((2019, 6, 29), 'Piotra i Pawła', ('Graduale', ), ('GradualeP', 'Tractus')),
])
def test_correct_gradual_tract_depending_on_the_season(date_, title_part, sections_present, sections_absent):
    missal = get_missal(date_[0], language)
    proper_vernacular, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    assert title_part in proper_vernacular.title
    for section in sections_present:
        assert proper_vernacular.get_section(section) is not None
        assert proper_latin.get_section(section) is not None
    for section in sections_absent:
        assert proper_vernacular.get_section(section) is None
        assert proper_latin.get_section(section) is None
