import json
import pytest
from datetime import date

from api.constants.common import *
from api.exceptions import InvalidInput, ProperNotFound

from api.constants import common as c
from api.kalendar.models import Observance
from api.propers.models import ProperConfig
from api.propers.parser import ProperParser
from .conftest import get_missal, HERE

language = 'pl'


def test_parse_proper_no_refs():
    proper_vernacular, proper_latin = ProperParser(c.SANCTI_01_06, language).parse()

    assert 'Objawienie' in proper_vernacular.title
    assert 1 == proper_vernacular.rank
    assert '«Obchodzimy dzień święty' in proper_vernacular.description
    assert 'Stacja u Św. Piotra' in proper_vernacular.tags
    assert 'Szaty białe' in proper_vernacular.tags
    assert 'Ml 3:1' in proper_vernacular.get_section(INTROIT).body[0]
    assert 'Boże, w dniu dzisiejszym' in proper_vernacular.get_section(ORATIO).body[0]
    assert '*Iz 60:1-6*' in proper_vernacular.get_section(LECTIO).body[1]
    assert 'Iz 60:6; 60:1' in proper_vernacular.get_section(GRADUALE).body[0]
    assert '*Mt 2:1-12*' in proper_vernacular.get_section(EVANGELIUM).body[1]
    assert 'Ps 71:10-11' in proper_vernacular.get_section(OFFERTORIUM).body[0]
    assert 'Wejrzyj miłościwie' in proper_vernacular.get_section(SECRETA).body[0]
    assert 'Mt 2:2' in proper_vernacular.get_section(COMMUNIO).body[0]
    assert 'Spraw, prosimy,' in proper_vernacular.get_section(POSTCOMMUNIO).body[0]
    assert 'Prefacja o Objawieniu' in proper_vernacular.get_section(PREFATIO).body[0]

    assert 'Malach 3:1' in proper_latin.get_section(INTROIT).body[0]
    assert 'Deus, qui hodiérna die' in proper_latin.get_section(ORATIO).body[0]
    assert '*Is 60:1-6*' in proper_latin.get_section(LECTIO).body[1]
    assert '*Isa 60:6; 60:1*' in proper_latin.get_section(GRADUALE).body[0]
    assert '*Matt 2:1-12*' in proper_latin.get_section(EVANGELIUM).body[1]
    assert '*Ps 71:10-11*' in proper_latin.get_section(OFFERTORIUM).body[0]
    assert 'Ecclésiæ tuæ, quǽsumus' in proper_latin.get_section(SECRETA).body[0]
    assert '*Matt 2:2*' in proper_latin.get_section(COMMUNIO).body[0]
    assert 'Præsta, quǽsumus, omnípotens' in proper_latin.get_section(POSTCOMMUNIO).body[0]
    assert '*de Epiphania Domini*' in proper_latin.get_section(PREFATIO).body[0]


def test_parse_proper_refs_inside_sections_and_in_vide():
    proper_vernacular, proper_latin = ProperParser(c.SANCTI_01_22, language).parse()

    assert 'Śś. Wincentego' in proper_vernacular.title
    assert '*Ps 78:11-12; 78:10*' in proper_vernacular.get_section(INTROIT).body[0]
    assert 'Przychyl się, Panie,' in proper_vernacular.get_section(ORATIO).body[0]
    assert '*Mdr 3:1-8*' in proper_vernacular.get_section(LECTIO).body[1]
    assert '*Wj 15:11*' in proper_vernacular.get_section(GRADUALE).body[0]
    assert '*Wj 15:11*' in proper_vernacular.get_section(TRACTUS).body[0]
    assert '*Łk 21:9-19*' in proper_vernacular.get_section(EVANGELIUM).body[1]
    assert '*Ps 67:36*' in proper_vernacular.get_section(OFFERTORIUM).body[0]
    assert 'Ofiarujemy Ci, Panie, te dary' in proper_vernacular.get_section(SECRETA).body[0]
    assert '*Mdr 3:4-6*' in proper_vernacular.get_section(COMMUNIO).body[0]
    assert 'Prosimy Cię, wszechmogący' in proper_vernacular.get_section(POSTCOMMUNIO).body[0]
    assert 'Prefacja zwykła' in proper_vernacular.get_section(PREFATIO).body[0]

    assert '*Ps 78:11-12; 78:10*' in proper_latin.get_section(INTROIT).body[0]
    assert 'Adésto, Dómine, supplicatiónibus' in proper_latin.get_section(ORATIO).body[0]
    assert '*Sap 3:1-8*' in proper_latin.get_section(LECTIO).body[1]
    assert '*Exod 15:11*' in proper_latin.get_section(GRADUALE).body[0]
    assert '*Exod 15:11*' in proper_latin.get_section(TRACTUS).body[0]
    assert '*Luc 21:9-19*' in proper_latin.get_section(EVANGELIUM).body[1]
    assert '*Ps 67:36*' in proper_latin.get_section(OFFERTORIUM).body[0]
    assert 'Múnera tibi, Dómine,' in proper_latin.get_section(SECRETA).body[0]
    assert '*Sap 3:4-6*' in proper_latin.get_section(COMMUNIO).body[0]
    assert 'Quǽsumus, omnípotens Deus:' in proper_latin.get_section(POSTCOMMUNIO).body[0]
    assert '*Communis*' in proper_latin.get_section(PREFATIO).body[0]


def test_parse_proper_ref_outside_sections():
    proper_vernacular, proper_latin = ProperParser(c.SANCTI_10_DU, language).parse()
    assert 'Chrystusa Króla' in proper_vernacular.title
    assert '*Ap 5:12; 1:6*' in proper_vernacular.get_section(INTROIT).body[0]
    assert '*Apoc 5:12; 1:6*' in proper_latin.get_section(INTROIT).body[0]


def test_invalid_proper_id():
    with pytest.raises(InvalidInput):
        ProperParser('bla', language).parse()


def test_proper_not_found():
    with pytest.raises(ProperNotFound):
        ProperParser('tempora:bla', language).parse()


def test_get_proper_from_observance():
    proper_vernacular, proper_latin = Observance(c.SANCTI_01_06, date(2018, 1, 6), language).get_proper()
    assert 'Objawienie' in proper_vernacular.title
    assert 'Ml 3:1' in proper_vernacular.get_section(INTROIT).body[0]
    assert 'Malach 3:1' in proper_latin.get_section(INTROIT).body[0]
    assert 'Deus, qui hodiérna die' in proper_latin.get_section(ORATIO).body[0]


def test_get_proper_from_day():
    missal = get_missal(2018, language)
    proper_vernacular, proper_latin = missal.get_day(date(2018, 1, 6)).get_proper()[0]
    assert 'Objawienie' in proper_vernacular.title
    assert 'Ml 3:1' in proper_vernacular.get_section(INTROIT).body[0]
    assert 'Malach 3:1' in proper_latin.get_section(INTROIT).body[0]
    assert 'Deus, qui hodiérna die' in proper_latin.get_section(ORATIO).body[0]


@pytest.mark.parametrize("date_,id_,rank", [
    ((2018, 1, 4), SANCTI_01_01, 4),
    ((2019, 1, 3), SANCTI_01_01, 4),  # Feria between Holy Name and Epiphany -> Octave of the Nativity
    ((2021, 1, 4), SANCTI_01_01, 4),  # Feria between Holy Name and Epiphany -> Octave of the Nativity
    ((2021, 1, 5), SANCTI_01_01, 4),  # Feria between Holy Name and Epiphany -> Octave of the Nativity
    ((2019, 1, 7), SANCTI_01_06, 4),  # Feria between Epiphany and next Sunday -> Epiphany
    ((2021, 1, 7), SANCTI_01_06, 4),  # Feria between Epiphany and next Sunday -> Epiphany
    ((2021, 1, 8), SANCTI_01_06, 4),  # Feria between Epiphany and next Sunday -> Epiphany
    ((2018, 1, 12), TEMPORA_EPI1_0A, 4),  # Feast of the Holy Family
    ((2018, 2, 13), TEMPORA_QUADP3_0, 4),
    ((2018, 7, 4), TEMPORA_PENT06_0, 4),
    ((2018, 7, 9), TEMPORA_PENT07_0, 4),  # Feast of the Most Precious Blood
    ((2018, 10, 31), TEMPORA_PENT23_0, 4),  # Feast of Christ the King
])
def test_get_proper_for_day_without_own_proper(date_, id_, rank):
    # For days without their own propers we show the proper from the last Sunday
    missal = get_missal(date_[0], language)
    _, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    assert id_ == proper_latin.id == id_
    assert rank == proper_latin.rank


def test_get_repr():
    missal = get_missal(2018, language)
    container = missal.get_day(date(2018, 1, 13))
    assert 'Sobota po 1 Niedzieli po Objawieniu' in container.get_tempora_name()
    assert 'Wspomnienie Chrztu Pańskiego' in container.get_celebration_name()
    assert str(container) == '[<tempora:Epi1-6:4:w>][<sancti:01-13:2:w>][]'


@pytest.mark.parametrize("date_,sections", [
    ((2018, 12, 6), ['Rank1570']),
    ((2019, 3, 25), [GRADUALE])
])
def test_ignored_sections(date_, sections):
    missal = get_missal(date_[0], language)
    _, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    for section in sections:
        assert proper_latin.get_section(section) is None


@pytest.mark.parametrize("date_,title_part,preface_body", [
    ((2018, 10, 28), 'Chrystusa Króla', '*de D.N. Jesu Christi Rege*'),
    ((2018, 12, 16), '3 Niedziela Adwentu', '*de sanctissima Trinitate*'),
    ((2018, 12, 17), 'Poniedziałek po 3 Niedzieli Adwentu', '*Communis*'),
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
    assert preface_body == proper_latin.get_section(PREFATIO).get_body()[0]


@pytest.mark.parametrize("proper_id,preface_name,preface_body", [
    (TEMPORA_ADV2_0, 'Communis', '*Communis*'),
    (TEMPORA_ADV2_0, 'Trinitate', '*de sanctissima Trinitate*'),
])
def test_correct_preface_calculated_by_proper_id(proper_id, preface_name, preface_body):
    _, proper_latin = ProperParser(proper_id, language, ProperConfig(preface=preface_name)).parse()
    assert preface_body == proper_latin.get_section(PREFATIO).get_body()[0]


@pytest.mark.parametrize("proper_id,preface_body_fragment_v,preface_body_fragment_lat", [
    (SANCTI_05_31, 'obchodząc święto Najświętszej', 'Et te in festivitate beátæ'),  # BVM the Queen
    (SANCTI_08_15, 'obchodząc Wniebowzięcie Najświętszej', 'Et te in Assumptióne beátæ'),
    (SANCTI_12_08, 'obchodząc Niepokalane Poczęcie Najświętszej', 'Et te in Conceptióne immaculáta beátæ'),
    (COMMUNE_C_10A, 'wysławiali czcząc Najświętszą Maryję', 'Et te in veneratione beátæ'),  # rorate
])
def test_preface_modifications(proper_id, preface_body_fragment_v, preface_body_fragment_lat):
    """
    For example for feasts of BVM the name of the feast changes depending on the current feast
    """
    proper_vernacular, proper_latin = ProperParser(proper_id, language).parse()
    assert preface_body_fragment_v in proper_vernacular.get_section(PREFATIO).serialize()['body']
    assert preface_body_fragment_lat in proper_latin.get_section(PREFATIO).serialize()['body']


@pytest.mark.parametrize("date_,title_part,sections_present,sections_absent", [
    ((2019, 7, 3), 'Ireneusza', (GRADUALE, ), (GRADUALE_PASCHAL, TRACTUS)),
    ((2019, 6, 29), 'Piotra i Pawła', (GRADUALE, ), (GRADUALE_PASCHAL, TRACTUS)),
    ((2019, 1, 17), 'Antoniego', (GRADUALE, ), (GRADUALE_PASCHAL, TRACTUS)),  # Sancti/01-17 -> Commune/C4c; normal season
    ((2018, 2, 7), 'Romualda', (TRACTUS, ), (GRADUALE, GRADUALE_PASCHAL)),  # Sancti/01-17 -> Commune/C4c; pre-lent
    ((2019, 5, 10), 'Antonina', (GRADUALE_PASCHAL, ), (GRADUALE, TRACTUS)),  # Sancti/05-10 -> Commune/C4; paschal
    ((2018, 4, 14), 'Justyna', (GRADUALE_PASCHAL, ), (GRADUALE, TRACTUS)),  # Sancti/04-14 / paschal, but has no gradualep
    ((2019, 5, 2), 'Atanazego', (GRADUALE, ), (GRADUALE_PASCHAL, TRACTUS)),  # Sancti/04-14 / paschal, but has no gradualep
    ((2019, 2, 22), 'Katedry', (TRACTUS, ), (GRADUALE_PASCHAL, GRADUALE_PASCHAL)),
    ((2019, 2, 23), 'Piotra Damiana', (TRACTUS, ), (GRADUALE_PASCHAL, GRADUALE_PASCHAL)),
    ((2019, 4, 30), 'Katarzyny', (GRADUALE_PASCHAL, ), (TRACTUS, GRADUALE)),
    ((2019, 5, 10), 'Antonina', (GRADUALE_PASCHAL, ), (TRACTUS, GRADUALE)),
    ((2019, 5, 13), 'Bellarmina', (GRADUALE_PASCHAL, ), (TRACTUS, GRADUALE)),
    ((2019, 5, 17), 'Paschalisa', (GRADUALE_PASCHAL, ), (TRACTUS, GRADUALE)),

    ((2019, 8, 15), 'Wniebowzięcie', (GRADUALE, ), (TRACTUS, GRADUALE_PASCHAL)),
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


@pytest.mark.parametrize("date_,stripped", [
    ((2019, 7, 7), False),
    ((2019, 7, 9), True),
    ((2019, 9, 13), True)
])
def test_alleluia_stripped_in_gradual_in_feria_day_using_sunday_proper(date_, stripped):
    missal = get_missal(date_[0], language)
    proper_vernacular, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    gradual_vernacular = proper_vernacular.get_section(GRADUALE).body
    gradual_latin = proper_latin.get_section(GRADUALE).body
    assert any([PATTERN_ALLELUIA.search(i, re.I) for i in gradual_vernacular + gradual_latin]) is not stripped


@pytest.mark.parametrize("date_,stripped", [
    ((2020, 2, 9), False),
    ((2020, 2, 13), True),
    ((2020, 2, 14), True),
    ((2020, 2, 16), False),
    ((2020, 2, 17), True),
    ((2020, 2, 18), True),
    ((2020, 2, 23), False),
    ((2020, 2, 24), True),
])
def test_tract_stripped_in_gradual_in_feria_day_using_sunday_proper(date_, stripped):
    missal = get_missal(date_[0], language)
    proper_vernacular, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    gradual_vernacular = proper_vernacular.get_section(GRADUALE).body
    gradual_latin = proper_latin.get_section(GRADUALE).body
    assert any([re.search(re.compile(PATTERN_TRACT), i) for i in gradual_vernacular + gradual_latin]) is not stripped


@pytest.mark.parametrize("date_,collect_contains,secreta_contains,postcommunio_contains,"
                         "comm_collect_sub,comm_collect_contains,comm_secreta_contains,comm_postcommunio_contains", [
    # St. Matthias, Apostle, commemoration of Ember Saturday of Lent
    ((2018, 2, 24), "Deus qui beátum Matthíam", "Hóstias tibi, Dómine", "Præsta, quǽsumus, omnípotens",
                    "Commemoratio Sabbato Quattuor Temporum Quadragesimæ", "Pópulum tuum", "Præséntibus sacrifíciis", "Sanctificatiónibus tuis"),
    # Advent feria, commemoration of S. Thomæ de Aquino
    ((2019, 3, 7), "Deus, qui culpa offénderis", "Sacrifíciis præséntibus, Dómine", "Cœléstis doni benedictióne",
                    "Thomæ de Aquino", "Deus, qui Ecclésiam tuam", "Sancti Thomæ Confessóris tui", "Ut nobis, Dómine, tua sacrifícia"),
    # Advent feria, commemoration of S. Thomæ de Aquino
    ((2019, 9, 15), "Custódi, Dómine, quǽsumus", "Concéde nobis, Dómine", "Puríficent semper et múniant",
                    "Septem Dolorum", "Deus, in cujus passióne", "Offérimus tibi preces et", "Sacrifícia, quæ súmpsimus"),
    # Ember Friday of September, commemoration of S. Eustachii et Sociorum Martyrum
    ((2019, 9, 20), "Præsta, quǽsumus, omnípotens", "Accépta tibi sint, Dómine, quǽsumus", "Quǽsumus, omnípotens Deus",
                    "Eustachii", "Deus, qui nos concédis sanctórum", "Múnera tibi, Dómine, nostra", "Præsta nobis, quǽsumus, Dómine"),
    # S. Matthæi Apostoli, commemoration of Ember Saturday of September
    ((2019, 9, 21), "Beáti Apóstoli et Evangelístæ", "Supplicatiónibus beáti Matthæi", "Percéptis, Dómine, sacraméntis",
                    "Sabbato Quattuor Temporum Septembris", "Omnípotens sempitérne Deus", "Concéde, quǽsumus, omnípotens", "Perfíciant in nobis, Dómine"),
    # S. Michælis Archangelis, commemoration of Sunday
    ((2019, 9, 29), "Deus, qui, miro ordine", "Hóstias tibi, Dómine, laudis", "Beáti Archángeli tui Michaélis",
                    "Dominica XVI", "Tua nos, quǽsumus, Dómine", "Munda nos, quǽsumus", "Purífica, quǽsumus, Dómine"),
    # Sanctae Mariae Sabbato, commemoration of Ss. Placidi et Sociorum Martyrum
    ((2019, 10, 5), "Concéde nos fámulos tuos", "Tua, Dómine, propitiatióne", "Sumptis, Dómine, salútis",
                    "Placidi et Sociorum", "Deus, qui nos concédis sanctórum", "Adésto, Dómine, supplicatiónibus", "Præsta nobis, quǽsumus"),
    # Friday in Octave of Pentecost, commemoration of Quatuor Coronatorum Martyrum
    ((2019, 11, 8), "Famíliam tuam, quǽsumus", "Suscipe, Dómine, propítius", "Immortalitátis alimóniam",
                    "", "Præsta, quǽsumus, omnípotens", "Benedíctio tua, Dómine, larga", "Cœléstibus refécti sacraméntis"),
    # S. Francisci Xaverii Confessoris, commemoration of Advent day
    ((2019, 12, 3), "Deus, qui Indiárum", "Præsta nobis, quǽsumus", "Quǽsumus, omnípotens Deus:",
                    "Feria III infra Hebd I Adventus", "Excita, quǽsumus, Dómine", "Hæc sacra nos, Dómine", "Suscipiámus, Dómine, misericórdiam"),
    # In Conceptione Immaculata Beatæ Mariæ Virginis, commemoration of the Sunday
    ((2019, 12, 8), "Deus, qui per immaculátam Vírginis", "Salutárem hóstiam, quam", "Sacraménta quæ súmpsimus",
                    "Dominica II Adventus", "Excita, Dómine, corda nostra", "Placáre, quǽsumus, Dómine", "Repléti cibo spirituális alimóniæ"),
    # S. Thomæ Apostoli, commemoration of Ember Saturday of Advent
    ((2019, 12, 21), "Da nobis, quǽsumus, Dómine,", "Débitum tibi, Dómine, nostræ", "Adésto nobis, miséricors Deus",
                     "Commemoratio Sabbato", "Deus, qui cónspicis, quia", "Sacrifíciis præséntibus, quǽsumus", "Quǽsumus, Dómine, Deus"),
    # Double commemoration
    ((2023, 1, 19), "Omnípotens sempitérne Deus", "Oblata, Dómine, múnera", "Augeátur in nobis",
                    "S. Marii et Soc. Mart.", "Exáudi, Dómine, pópulum tuum", "S. Canuto Regi Mart.", "S. Marii et Soc. Mart."),
])
def test_calculated_commemorations(date_, collect_contains,secreta_contains,postcommunio_contains,
                                   comm_collect_sub, comm_collect_contains, comm_secreta_contains,
                                   comm_postcommunio_contains):
    missal = get_missal(date_[0], language)
    proper_vernacular, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    assert collect_contains in proper_latin.get_section(ORATIO).serialize()["body"]
    assert comm_collect_contains in proper_latin.get_section(COMMEMORATED_ORATIO).serialize()["body"]
    assert comm_collect_sub in proper_latin.get_section(COMMEMORATED_ORATIO).serialize()["body"]
    assert secreta_contains in proper_latin.get_section(SECRETA).serialize()["body"]
    assert comm_secreta_contains in proper_latin.get_section(COMMEMORATED_SECRETA).serialize()["body"]
    assert postcommunio_contains in proper_latin.get_section(POSTCOMMUNIO).serialize()["body"]
    assert comm_postcommunio_contains in proper_latin.get_section(COMMEMORATED_POSTCOMMUNIO).serialize()["body"]


@pytest.mark.parametrize("date_,introit,collect,lectio,gradual,evangelium,offertorium,secreta,communio,postcommunio", [
    # 4th Sunday after Epiphany moved to the period after Pentecost
    ((2018, 11, 4), "Jer 29:11; 29:12; 29:14", "Deus, qui nos", "Rom 13:8-10", "Ps 43:8-9", "Matt 8:23-27",
     "Ps 129:1-2", "Concéde, quǽsumus", "Marc 11:24", "Múnera tua nos"),
    # Monday after 4th Sunday after Epiphany moved to the period after Pentecost
    ((2018, 11, 5), "Jer 29:11; 29:12; 29:14", "Deus, qui nos", "Rom 13:8-10", "Ps 43:8-9", "Matt 8:23-27",
     "Ps 129:1-2", "Concéde, quǽsumus", "Marc 11:24", "Múnera tua nos"),
    # 5th Sunday after Epiphany moved to the period after Pentecost
    ((2018, 11, 11), "Jer 29:11; 29:12; 29:14", "Famíliam tuam", "Col 3:12-17", "Ps 43:8-9", "Matt 13:24-30",
     "Ps 129:1-2", "Hóstias tibi", "Marc 11:24", "Quǽsumus, omnípotens"),
    # 6th Sunday after Epiphany moved to the period after Pentecost
    ((2018, 11, 18), "Jer 29:11; 29:12; 29:14", "Præsta, quǽsumus", "1 Thess 1:2-10", "Ps 43:8-9", "Matt 13:31-35",
     "Ps 129:1-2", "Hæc nos oblátio", "Marc 11:24", "Cœléstibus, Dómine"),
])
def test_sundays_shifted_from_post_epiphany_to_post_pentecost_have_proper_sections(
        date_, introit, collect, lectio, gradual, evangelium, offertorium, secreta, communio, postcommunio):
    missal = get_missal(date_[0], language)
    proper_vernacular, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    assert introit in proper_latin.get_section(INTROIT).body[0]
    assert collect in proper_latin.get_section(ORATIO).body[0]
    assert lectio in proper_latin.get_section(LECTIO).body[1]
    assert gradual in proper_latin.get_section(GRADUALE).body[0]
    assert evangelium in proper_latin.get_section(EVANGELIUM).body[1]
    assert offertorium in proper_latin.get_section(OFFERTORIUM).body[0]
    assert secreta in proper_latin.get_section(SECRETA).body[0]
    assert communio in proper_latin.get_section(COMMUNIO).body[0]


@pytest.mark.parametrize("date_", [
    (2020, 8, 20),
    (2020, 1, 12)
])
def test_excluded_commemorations(date_):
    missal = get_missal(date_[0], language)
    proper_vernacular, proper_latin = missal.get_day(date(*date_)).get_proper()[0]
    for stripped_section in (COMMEMORATED_ORATIO, COMMEMORATED_SECRETA, COMMEMORATED_POSTCOMMUNIO):
        assert None is proper_vernacular.get_section(stripped_section)
        assert None is proper_latin.get_section(stripped_section)

@pytest.mark.parametrize("date_,prop1_commemoration,prop2_commemoration", [
    ((2024, 3, 7), "Wspomnienie Św. Tomasza z Akwinu", "Wspomnienie Czwartek po 3 Niedzieli Wielkiego Postu"),
    ((2024, 3, 21), "Wspomnienie Św. Benedykta, Opata", "Wspomnienie Czwartek po Niedzieli Męki Pańskiej")
])
def test_multiple_celebrations_with_multiple_commemorations(date_, prop1_commemoration, prop2_commemoration):
    """
    On Lent feria days either feria proper with saint's commemoration can be used
    or vice versa - saint's proper with feria day's commemoration
    """
    missal = get_missal(date_[0], language)
    proper = missal.get_day(date(*date_)).get_proper()
    vern1, _ = proper[0]
    vern2, _ = proper[1]
    assert prop1_commemoration in vern1.get_section(COMMEMORATED_ORATIO).body[0]
    assert prop2_commemoration in vern2.get_section(COMMEMORATED_ORATIO).body[0]


def _get_proper_fixtures(fixture):
    with open(os.path.join(HERE, 'fixtures/{}'.format(fixture))) as fh:
        # return [i for i in json.load(fh).items() if i[0][5:] >= '01-01' and i[0][5:] <= '02-23']
        return list(json.load(fh).items())


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
