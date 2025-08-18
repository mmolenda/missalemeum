import os
import datetime
import json
from collections import defaultdict

from conftest import get_missal

HERE = os.path.abspath(os.path.dirname(__file__))
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


def generate_propers_fixtures(dates: list[datetime.date], language: str):
    coll = defaultdict(list)
    for dt in dates:
        strdt = dt.strftime("%Y-%m-%d")
        print(f"{language}/{strdt}")
        missal = get_missal(dt.year, language if language != "la" else "pl")
        day = missal.get_day(dt)
        if language == "la":
            _, proper = day.get_proper()[0]
        else:
            proper, _ = day.get_proper()[0]
        srlzd = proper.serialize()
        for section in srlzd:
            coll[strdt].append({"id": section["id"], "body": section["body"][:120]})
    with open(f'fixtures/propers_{language}.json', 'w') as fh:
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
        missal = get_missal(dt.year, language if language != "la" else "pl")
        day = missal.get_day(dt)
        if language == "la":
            _, proper = day.get_proper()[0]
        else:
            proper, _ = day.get_proper()[0]
        srlzd = proper.serialize()
        coll[strdt] = [{"id": section["id"], "body": section["body"][:120]} for section in srlzd]

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
    # compare_years(2024, 2025, "en")
    # for l in ['la', 'pl', 'en']:
        # generate_propers_fixtures(dates, l)

    lang = "en"
    
    update_propers_for_dates(
        [datetime.date(2024, 1, 22), datetime.date(2025, 1, 22)],
        lang,
        os.path.join(HERE, "fixtures", f"propers_{lang}.json")
    )
