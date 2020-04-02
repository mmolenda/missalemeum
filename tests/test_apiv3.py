import json
import os
from datetime import date, timedelta

import pytest

from conftest import HERE
from constants.common import LANGUAGES


def test_api_calendar(client):
    with open(os.path.join(HERE, 'fixtures/api_calendar_2020.json')) as fh:
        expected = json.load(fh)
    resp = client.get('/pl/api/v3/calendar/2020').json
    assert expected.keys() == resp.keys()
    for date_, data in expected.items():
        assert data == resp[date_]


def test_api_date(client):
    resp = client.get('/pl/api/v3/date/2020-11-11').json
    info = resp[0]["info"]
    assert ["Szaty białe"] == info["additional_info"]
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
        date_ = date(2020, 4, 1)
        i = 0
        while i < 365:
            yield lang, date_.strftime("%Y-%m-%d")
            date_ += timedelta(days=1)
            i += 1


@pytest.mark.parametrize("lang,strdate", _get_dates())
def test_api_date_whole_year(client, lang, strdate):
    resp = client.get(f'/{lang}/api/v3/date/{strdate}')
    assert 200 == resp.status_code


def test_api_date_invalid_input(client):
    resp = client.get('/pl/api/v3/date/2020-11-99')
    assert 400 == resp.status_code
    assert {"error": "Incorrect date format, should be %Y-%m-%d"} == resp.json


def test_api_proper(client):
    resp = client.get('/pl/api/v3/proper/sancti:11-11:3:w').json
    info = resp[0]["info"]
    assert ["Szaty białe"] == info["additional_info"]
    assert ["w"] == info["colors"]
    assert "Św. Marcin urodził się około roku 316" in info["description"]
    assert "sancti:11-11:3:w" == info["id"]
    assert 3 == info["rank"]
    assert "Św. Marcina, Biskupa i Wyznawcy" == info["title"]
    assert "*Syr 45:30" in resp[0]["sections"][0]["body"][0][0]
    assert "*Eccli 45:30" in resp[0]["sections"][0]["body"][0][1]


def test_api_proper_slug(client):
    resp = client.get('/pl/api/v3/proper/rorate').json
    info = resp[0]["info"]
    assert ['Szaty białe', 'Adwent'] == info["additional_info"]
    assert ["w"] == info["colors"]
    assert "commune:C10a:0:w" == info["id"]
    assert '1 Msza o N. M. P. – Rorate' == info["title"]


def test_api_proper_invalid_input(client):
    resp = client.get('/pl/api/v3/proper/sancti:11-11')
    assert 404 == resp.status_code
    assert {"error": "Proper sancti:11-11 not found"} == resp.json


def test_api_supplement(client):
    resp = client.get('/pl/api/v3/supplement/2-adwent').json
    assert "Adwent" == resp["title"]
    assert "<h1>Adwent</h1>\n<p>Rok kościelny" in resp["body"]


def test_api_supplement_subdir(client):
    resp = client.get('/pl/api/v3/supplement/canticum/adoro-te').json
    assert "Adoro Te" == resp["title"]
    assert ["Eucharystyczne", "Łacińskie"] == resp["tags"]
    assert "ADORO TE, devote, latens Deitas" in resp["body"]


def test_api_supplement_missing(client):
    resp = client.get('/pl/api/v3/supplement/bla')
    assert 404 == resp.status_code
    assert {"error": "Not found"} == resp.json


def test_api_icalendar(client):
    resp = client.get('/pl/api/v3/icalendar')
    assert 200 == resp.status_code
    assert "text/calendar; charset=utf-8" == resp.content_type
    assert b"BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Missale Meum - Calendar//missalemeum.com//\r\n" in resp.data
