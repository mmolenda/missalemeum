import datetime
import json
from collections import defaultdict

from conftest import get_missal

year = 2020
lang = "la"


def generate_propers_fixtures(year: int, language: str):
    dt = datetime.date(year, 1, 1)
    coll = defaultdict(list)
    missal = get_missal(year, language if language != "la" else "pl")
    while dt.year == year:
        print(dt)
        day = missal.get_day(dt)
        if language == "la":
            _, proper = day.get_proper()[0]
        else:
            proper, _ = day.get_proper()[0]
        strdt = dt.strftime("%Y-%m-%d")
        srlzd = proper.serialize()
        for section in srlzd:
            coll[strdt].append({"id": section["id"], "body": section["body"][:120]})
        dt += datetime.timedelta(days=1)
    with open(f'fixtures/propers_{lang}_{year}.json', 'w') as fh:
        json.dump(coll, fh, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    generate_propers_fixtures(year, lang)
