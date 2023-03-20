import json
import os
from datetime import date, timedelta

import pytest

from .conftest import HERE
from constants.common import LANGUAGES


def test_api_calendar(client):
    with open(os.path.join(HERE, 'fixtures/api_calendar_v5_2023.json')) as fh:
        expected = json.load(fh)
    resp = client.get('/pl/api/v5/calendar/2023').json
    for i, item in enumerate(resp):
        assert item == expected[i]


def test_api_date(client):
    resp = client.get('/pl/api/v5/proper/2020-11-11').json
    info = resp[0]["info"]
    assert ['Szaty białe', 'Pallotinum s. 1186'] == info["tags"]
    assert ["w"] == info["colors"]
    assert "2020-11-11" == info["date"]
    assert "Św. Marcin urodził się około roku 316" in info["description"]
    assert "sancti:11-11:3:w" == info["id"]
    assert 3 == info["rank"]
    assert [] == info["supplements"]
    assert "Środa po 23 Niedzieli po Zesłaniu Ducha Świętego" == info["tempora"]
    assert "Św. Marcina, Biskupa i Wyznawcy" == info["title"]
    assert "*Syr 45:30" in resp[0]["sections"][0]["body"][0][0]
    assert "*Eccli 45:30" in resp[0]["sections"][0]["body"][0][1]


def _get_dates():
    for lang in LANGUAGES.keys():
        date_ = date(2020, 7, 1)
        i = 0
        while i < 365:
            yield lang, date_.strftime("%Y-%m-%d")
            date_ += timedelta(days=1)
            i += 1


@pytest.mark.parametrize("lang,strdate", _get_dates())
def test_api_date_whole_year(client, lang, strdate):
    resp = client.get(f'/{lang}/api/v5/proper/{strdate}')
    assert 200 == resp.status_code


@pytest.mark.parametrize("lang,slug", [
    ('en', 'tempore-mortalitatis'),
    ('en', 'rorate'),
    ('en', 'vultum-tuum'),
    ('en', 'salve-sancta-parens-3'),
    ('en', 'salve-sancta-parens-4'),
    ('en', 'salve-sancta-parens-5'),
    ('en', 'trinitas'),
    ('en', 'angelis'),
    ('en', 'joseph'),
    ('en', 'aeterno-sacerdote'),
    ('en', 'cordis-jesu'),
    ('en', 'cordis-mariae'),
    ('pl', 'tempore-mortalitatis'),
    ('pl', 'rorate'),
    ('pl', 'vultum-tuum'),
    ('pl', 'salve-sancta-parens-3'),
    ('pl', 'salve-sancta-parens-4'),
    ('pl', 'salve-sancta-parens-5'),
    ('pl', 'trinitas'),
    ('pl', 'angelis'),
    ('pl', 'joseph'),
    ('pl', 'petrus-et-paulus'),
    ('pl', 'petrus-et-paulus-p'),
    ('pl', 'apostolorum'),
    ('pl', 'apostolorum-p'),
    ('pl', 'spiritus-sanctus'),
    ('pl', 'spiritus-sanctus-2'),
    ('pl', 'eucharistiae-sacramento'),
    ('pl', 'aeterno-sacerdote'),
    ('pl', 'sancta-cruce'),
    ('pl', 'passio'),
    ('pl', 'cordis-jesu'),
    ('pl', 'cordis-mariae'),
    ('pl', 'fidei-propagatione'),
    ('pl', 'matrimonium'),
    ('pl', 'defunctorum'),
])
def test_api_votive(client, lang, slug):
    resp = client.get(f'/{lang}/api/v5/proper/{slug}')
    assert 200 == resp.status_code


def test_api_date_invalid_input(client):
    resp = client.get('/pl/api/v5/proper/2020-11-99')
    assert 404 == resp.status_code


def test_api_proper(client):
    resp = client.get('/pl/api/v5/proper/sancti:11-11:3:w').json
    info = resp[0]["info"]
    assert ['Szaty białe', 'Pallotinum s. 1186'] == info["tags"]
    assert ["w"] == info["colors"]
    assert "Św. Marcin urodził się około roku 316" in info["description"]
    assert "sancti:11-11:3:w" == info["id"]
    assert 3 == info["rank"]
    assert "Św. Marcina, Biskupa i Wyznawcy" == info["title"]
    assert "*Syr 45:30" in resp[0]["sections"][0]["body"][0][0]
    assert "*Eccli 45:30" in resp[0]["sections"][0]["body"][0][1]


def test_api_proper_slug(client):
    resp = client.get('/pl/api/v5/proper/rorate').json
    info = resp[0]["info"]
    assert ['Szaty białe', 'Adwent', 'Pallotinum s. 649'] == info["tags"]
    assert ["w"] == info["colors"]
    assert "commune:C10a:0:w" == info["id"]
    assert '1 Msza o N. M. P. – Rorate' == info["title"]


def test_api_proper_invalid_input(client):
    resp = client.get('/pl/api/v5/proper/sancti:11-11')
    assert 404 == resp.status_code
    assert {"error": "Proper sancti:11-11 not found"} == resp.json


def test_api_supplement(client):
    resp = client.get('/pl/api/v5/supplement/2-adwent').json
    assert "Adwent" == resp[0]['info']['title']
    assert resp[0]['sections'][0]['body'][0][0].startswith("Rok kościelny dzieli się na")


def test_api_supplement_subdir(client):
    resp = client.get('/pl/api/v5/canticum/adoro-te').json
    assert "Adoro Te" == resp[0]['info']['title']
    assert ["Eucharystyczne", "Łacińskie"] == resp[0]['info']['tags']
    assert "ADORO TE, devote, latens Deitas" in resp[0]['sections'][0]['body'][0][0]


def test_api_supplement_missing(client):
    resp = client.get('/pl/api/v5/supplement/bla')
    assert 404 == resp.status_code
    assert {"error": "Not found"} == resp.json


def test_api_icalendar(client):
    resp = client.get('/pl/api/v5/icalendar')
    assert 200 == resp.status_code
    assert "text/calendar; charset=utf-8" == resp.content_type
    assert b"BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Missale Meum - Calendar//missalemeum.com//\r\n" in resp.data
