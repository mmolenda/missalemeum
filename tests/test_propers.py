
import pytest

from exceptions import InvalidInput, ProperNotFound
from missal1962 import constants as c
from parsers import ProperParser


def test_parse_proper_no_refs():
    proper_vernacular, proper_latin = ProperParser.run(c.SANCTI_01_06, 'Polski')

    assert 'Objawienie' in proper_vernacular['Comment'].body[0]
    assert 'Ml 3:1' in proper_vernacular['Introitus'].body[0]
    assert 'Boże, w dniu dzisiejszym' in proper_vernacular['Oratio'].body[0]
    assert '*Iz 60:1-6*' in proper_vernacular['Lectio'].body[1]
    assert 'Iz 60:6; 60:1' in proper_vernacular['Graduale'].body[0]
    assert '*Mt 2:1-12*' in proper_vernacular['Evangelium'].body[1]
    assert 'Ps 71:10-11' in proper_vernacular['Offertorium'].body[0]
    assert 'Wejrzyj miłościwie' in proper_vernacular['Secreta'].body[0]
    assert 'Mt 2:2' in proper_vernacular['Communio'].body[0]
    assert 'Spraw, prosimy,' in proper_vernacular['Postcommunio'].body[0]
    assert 'Prefacja o Objawieniu' in proper_vernacular['Prefatio'].body[0]

    assert 'Malach 3:1' in proper_latin['Introitus'].body[0]
    assert 'Deus, qui hodiérna die' in proper_latin['Oratio'].body[0]
    assert '*Is 60:1-6*' in proper_latin['Lectio'].body[1]
    assert '*Isa 60:6; 60:1*' in proper_latin['Graduale'].body[0]
    assert '*Matt 2:1-12*' in proper_latin['Evangelium'].body[1]
    assert '*Ps 71:10-11*' in proper_latin['Offertorium'].body[0]
    assert 'Ecclésiæ tuæ, quǽsumus' in proper_latin['Secreta'].body[0]
    assert '*Matt 2:2*' in proper_latin['Communio'].body[0]
    assert 'Præsta, quǽsumus, omnípotens' in proper_latin['Postcommunio'].body[0]
    assert '*de Epiphania Domini*' in proper_latin['Prefatio'].body[0]


def test_parse_proper_refs_inside_sections_and_in_vide():
    proper_vernacular, proper_latin = ProperParser.run(c.SANCTI_01_22, 'Polski')

    assert '## 22 I – ŚŚ. Wincentego' in proper_vernacular['Comment'].body[0]
    assert '*Ps 78:11-12; 78:10*' in proper_vernacular['Introitus'].body[0]
    assert 'Przychyl się, Panie,' in proper_vernacular['Oratio'].body[0]
    assert '*Mdr 3:1-8*' in proper_vernacular['Lectio'].body[1]
    assert '*Wj 15:11*' in proper_vernacular['Graduale'].body[0]
    assert '*Wj 15:11*' in proper_vernacular['Tractus'].body[0]
    assert '*Łk 21:9-19*' in proper_vernacular['Evangelium'].body[1]
    assert '*Ps 67:36*' in proper_vernacular['Offertorium'].body[0]
    assert 'Ofiarujemy Ci, Panie, te dary' in proper_vernacular['Secreta'].body[0]
    assert '*Mdr 3:4-6*' in proper_vernacular['Communio'].body[0]
    assert 'Prosimy Cię, wszechmogący' in proper_vernacular['Postcommunio'].body[0]
    assert 'Prefacja zwykła' in proper_vernacular['Prefatio'].body[0]

    assert '*Ps 78:11-12; 78:10*' in proper_latin['Introitus'].body[0]
    assert 'Adésto, Dómine, supplicatiónibus' in proper_latin['Oratio'].body[0]
    assert '*Sap 3:1-8*' in proper_latin['Lectio'].body[1]
    assert '*Exod 15:11*' in proper_latin['Graduale'].body[0]
    assert '*Exod 15:11*' in proper_latin['Tractus'].body[0]
    assert '*Luc 21:9-19*' in proper_latin['Evangelium'].body[1]
    assert '*Ps 67:36*' in proper_latin['Offertorium'].body[0]
    assert 'Múnera tibi, Dómine,' in proper_latin['Secreta'].body[0]
    assert '*Sap 3:4-6*' in proper_latin['Communio'].body[0]
    assert 'Quǽsumus, omnípotens Deus:' in proper_latin['Postcommunio'].body[0]
    assert '*Communis*' in proper_latin['Prefatio'].body[0]


def test_parse_proper_ref_outside_sections():
    proper_vernacular, proper_latin = ProperParser.run(c.SANCTI_10_DUr, 'Polski')
    assert '## Chrystusa Króla' in proper_vernacular['Comment'].body[0]
    assert '*Ap 5:12; 1:6*' in proper_vernacular['Introitus'].body[0]
    assert '*Apoc 5:12; 1:6*' in proper_latin['Introitus'].body[0]


def test_invalid_proper_id():
    with pytest.raises(InvalidInput):
        ProperParser.run('bla', 'Polski')


def test_proper_not_found():
    with pytest.raises(ProperNotFound):
        ProperParser.run('tempora:bla', 'Polski')
