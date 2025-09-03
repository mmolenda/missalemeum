from collections import defaultdict
import os
import datetime
import json
import os
from api import controller
from api.constants import common as const

from tests.conftest import get_missal

here = os.path.abspath(os.path.dirname(__file__))
year_early_easter = 2024  # March 31
year_late_easter = 2025  # April 20

def get_dates(year):
    dates = []
    dt = datetime.date(year, 1, 1)
    while dt.year == year:
        dates.append(dt)
        dt += datetime.timedelta(days=1)
    return dates

dates = get_dates(year_early_easter)
dates.extend(get_dates(year_late_easter))


def generate_fixtures_for_propers_by_dates(dates: list[datetime.date], language: str):
    coll = {}
    for dt in dates:
        strdt = dt.strftime("%Y-%m-%d")
        print(f"{language}/{strdt}")
        missal = get_missal(dt.year, language if language != const.LANGUAGE_LATIN else const.LANGUAGE_POLSKI)
        day = missal.get_day(dt)
        for i, propers in enumerate(day.get_proper()):
            if strdt not in coll:
                coll[strdt] = []
            if len(coll[strdt]) < (i + 1):
                coll[strdt].append([])
                
            # one `propers` object per one mass in a day
            if language == const.LANGUAGE_LATIN:
                _, proper = propers
            else:
                proper, _ = propers
            srlzd = proper.serialize()
            for section in srlzd:
                coll[strdt][i].append({"id": section["id"], "body": section["body"][:120]})
    with open(os.path.join(here, f'fixtures/propers_{language}.json'), 'w') as fh:
        json.dump(coll, fh, indent=2, sort_keys=True, ensure_ascii=False)


def generate_fixtures_for_propers_by_ids(ids: list[str], language: str):
    coll = defaultdict(list)
    for proper_id in ids:
        propers_all: list[tuple] = [controller.get_proper_by_id(proper_id, language)]
        if language == const.LANGUAGE_LATIN:
            _, proper = propers_all[0]
        else:
            proper, _ = propers_all[0]
        srlzd = proper.serialize()
        for section in srlzd:
            coll[proper_id].append({"id": section["id"], "body": section["body"][:120]})
    with open(os.path.join(here, f'fixtures/propers_votive_{language}.json'), 'w') as fh:
        json.dump(coll, fh, indent=2, sort_keys=True, ensure_ascii=False)


def update_propers_for_dates(dates: list[datetime.date], language: str, fixture_path: str):
    # Load existing fixtures (if the file exists)
    if os.path.exists(fixture_path):
        with open(fixture_path, "r", encoding="utf-8") as fh:
            try:
                coll = json.load(fh)
            except json.JSONDecodeError:
                coll = {}
    else:
        coll = {}

    for dt in dates:
        strdt = dt.strftime("%Y-%m-%d")
        print(f"{language}/{strdt}")
        missal = get_missal(dt.year, language if language != const.LANGUAGE_LATIN else const.LANGUAGE_POLSKI)
        day = missal.get_day(dt)
        for i, propers in enumerate(day.get_proper()):
            if language == const.LANGUAGE_LATIN:
                _, proper = propers
            else:
                proper, _ = propers
            srlzd = proper.serialize()
            coll[strdt][i] = [{"id": section["id"], "body": section["body"][:120]} for section in srlzd]

    # Write updated data back to file
    with open(fixture_path, "w", encoding="utf-8") as fh:
        json.dump(coll, fh, indent=2, sort_keys=True, ensure_ascii=False)


def compare_years(y1, y2, lang):
    """
    Prints out nice comparison of two years in tabular format

    1-14   | Sunday     II Sunday after Epiphany       | Tuesday    St. Hilary
    1-15   | Monday     St. Paul, the First Hermit     | Wednesday  St. Paul, the First Hermit
    1-16   | Tuesday    St. Marcellus I                | Thursday   St. Marcellus I
    1-17   | Wednesday  St. Anthony                    | Friday     St. Anthony
    1-18   | Thursday   Feria                          | Saturday   II Mass of the B. V. M. – Vultum Tuum
    """
    collection = []
    missal1 = get_missal(y1, lang)
    missal2 = get_missal(y2, lang)
    for dt, day in missal1.items():
        try:
            dt2 = datetime.date(y2, dt.month, dt.day)
            day2 = missal2.get_day(dt2)
            collection.append([f"{dt.month}-{dt.day}",
                               dt.strftime("%A"),
                               day.celebration[0].title,
                               dt2.strftime("%A"),
                               day2.celebration[0].title])
        except ValueError as e:
            pass
    for c in collection:
        print(f"{c[0].ljust(6)} | {c[1].ljust(10)} {c[2][:40].ljust(42)} | {c[3].ljust(10)} {c[4][:40].ljust(42)}")


if __name__ == "__main__":
    # compare_years(2024, 2025, LANGUAGE_ENGLISH)
    # for l in ['la', 'pl', 'en']:
        # generate_propers_fixtures(dates, l)


    generate_fixtures_for_propers_by_ids(
        [
            const.COMMUNE_C_10A,
            const.COMMUNE_C_10B,
            const.COMMUNE_C_10C,
            const.COMMUNE_C_10PASC,
            const.COMMUNE_C_10T,
            const.VOTIVE_PENT01_0,
            const.VOTIVE_ANGELS,
            const.VOTIVE_JOSEPH,
            const.VOTIVE_PETERPAUL,
            const.VOTIVE_PETERPAULP,
            const.VOTIVE_APOSTLES,
            const.VOTIVE_APOSTLESP,
            const.VOTIVE_HOLYSPIRIT,
            const.VOTIVE_HOLYSPIRIT2,
            const.VOTIVE_BLESSEDSACRAMENT,
            const.VOTIVE_JESUSETERNALPRIEST,
            const.VOTIVE_CROSS,
            const.VOTIVE_PASSION,
            const.VOTIVE_PENT02_5,
            const.VOTIVE_08_22,
            const.VOTIVE_TERRIBILIS,
            const.VOTIVE_FIDEI_PROPAGATIONE,
            const.VOTIVE_DEFUNCTORUM,
            const.VOTIVE_MORTALITATIS,
        ]
        , const.LANGUAGE_POLSKI)
    

    generate_fixtures_for_propers_by_ids(
        [
            const.COMMUNE_C_10A,
            const.COMMUNE_C_10B,
            const.COMMUNE_C_10C,
            const.COMMUNE_C_10PASC,
            const.COMMUNE_C_10T,
            const.VOTIVE_PENT01_0,
            const.VOTIVE_ANGELS,
            const.VOTIVE_JOSEPH,
            const.VOTIVE_JESUSETERNALPRIEST,
            const.VOTIVE_PENT02_5,
            const.VOTIVE_08_22,
            const.VOTIVE_MORTALITATIS,
        ]
        , const.LANGUAGE_POLSKI)


    
    # update_propers_for_dates(
    #     [
    #     # datetime.date(2024, 2, 15),
    #      datetime.date(2025, 2, 15)
    #     ],
    #     lang,
    #     os.path.join(here, "fixtures", f"propers_{lang}.json")
    # )
