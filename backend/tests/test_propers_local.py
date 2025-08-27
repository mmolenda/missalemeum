import datetime
import json
import pytest
from datetime import date

from api.constants.common import *
from .util import update_propers_for_dates

from .conftest import get_missal, HERE

languages = [
    'pl',
    # 'en',
    # 'la'
    ]
years = [
    '2024',
    '2025',
]
days = [
    '05-11',
    # '05-02',
    # '05-01',
    ]


def _get_proper_fixtures(fixture):
    dates = [f"{y}-{d}" for y in years for d in days]
    with open(os.path.join(HERE, 'fixtures/{}'.format(fixture))) as fh:
        x = json.load(fh)
        # return [i for i in x.items() if i[0][5:] >= '01-01' and i[0][5:] <= '03-25']
        return [i for i in x.items() if i[0] in dates]

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
    propers = day.get_proper()
    for j, propers in enumerate(day.get_proper()):
        _, proper = propers
        proper_serialized = proper.serialize()
        context = ['Latin', strdate, f'mass{j}', proper.id, proper.title]
        assert [i['id'] for i in proper_serialized] == [i['id'] for i in expected_sections[j]], ' - '.join(context)
        for i, expected_section in enumerate(expected_sections[j]):
            expected_body = expected_section['body']
            actual_body = proper_serialized[i]['body']
            ok = actual_body.startswith(expected_body)
            if not ok:
                fix = f"\n+ # FIX =\n\n[{expected_section["id"]}]\n{actual_body}" if actual_body.startswith('@') else ""
                context2 = context.copy()
                context2.insert(4, f'[{expected_section["id"]}]')
                pytest.fail(
                    f"\n+ # CONTEXT: {' - '.join(context2)}"
                    f"\n+ # EXPECTED = {expected_body!r}"
                    f"\n+ # ACTUAL   = {actual_body[:len(expected_body)]!r}"
                    f"{fix}",
                    pytrace=False,
                )


@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures("propers_pl.json"))
def test_all_propers_polish(strdate, expected_sections):
    strdate_bits = [int(i) for i in strdate.split('-')]
    missal = get_missal(strdate_bits[0], 'pl')
    day = missal.get_day(date(*strdate_bits))
    propers = day.get_proper()
    for j, propers in enumerate(day.get_proper()):
        proper, _ = propers
        proper_serialized = proper.serialize()
        context = ['Polski', strdate, f'mass{j}', proper.id, proper.title]
        assert [i['id'] for i in proper_serialized] == [i['id'] for i in expected_sections[j]], ' - '.join(context)
        for i, expected_section in enumerate(expected_sections[j]):
            expected_body = expected_section['body']
            actual_body = proper_serialized[i]['body']
            ok = actual_body.startswith(expected_body)
            if not ok:
                fix = f"\n+ # FIX =\n\n[{expected_section["id"]}]\n{actual_body}" if actual_body.startswith('@') else ""
                context2 = context.copy()
                context2.insert(4, f'[{expected_section["id"]}]')
                pytest.fail(
                    f"\n+ # CONTEXT: {' - '.join(context2)}"
                    f"\n+ # EXPECTED = {expected_body!r}"
                    f"\n+ # ACTUAL   = {actual_body[:len(expected_body)]!r}"
                    f"{fix}",
                    pytrace=False,
                )


@pytest.mark.parametrize("strdate,expected_sections", _get_proper_fixtures("propers_en.json"))
def test_all_propers_english(strdate, expected_sections):
    strdate_bits = [int(i) for i in strdate.split('-')]
    missal = get_missal(strdate_bits[0], 'en')
    day = missal.get_day(date(*strdate_bits))
    propers = day.get_proper()
    for j, propers in enumerate(day.get_proper()):
        proper, _ = propers
        proper_serialized = proper.serialize()
        context = ['English', strdate, f'mass{j}', proper.id, proper.title]
        assert [i['id'] for i in proper_serialized] == [i['id'] for i in expected_sections[j]], ' - '.join(context)
        for i, expected_section in enumerate(expected_sections[j]):
            expected_body = expected_section['body']
            actual_body = proper_serialized[i]['body']
            ok = actual_body.startswith(expected_body)
            if not ok:
                fix = f"\n+ # FIX =\n\n[{expected_section["id"]}]\n{actual_body}" if actual_body.startswith('@') else ""
                context2 = context.copy()
                context2.insert(4, f'[{expected_section["id"]}]')
                pytest.fail(
                    f"\n+ # CONTEXT: {' - '.join(context2)}"
                    f"\n+ # EXPECTED = {expected_body!r}"
                    f"\n+ # ACTUAL   = {actual_body[:len(expected_body)]!r}"
                    f"{fix}",
                    pytrace=False,
                )


@pytest.mark.skip
def test_update_fixtures():
    for language in languages:
        dates_strs = [f"{y}-{d}" for y in years for d in days]
        datetimes = [datetime.date(*[int(j) for j in i.split('-')]) for i in dates_strs]
        update_propers_for_dates(
            datetimes,
            language,
            os.path.join(HERE, "fixtures", f"propers_{language}.json")
        )