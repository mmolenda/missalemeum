import os
import datetime
import json
import os
import sys
from api.constants import common as const

from tests.conftest import get_missal, HERE
from tests.test_propers_local import days, years

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


if __name__ == "__main__":
    languages = [i.strip() for i in sys.argv[1].split(" ")]
    dates_strs = [f"{y}-{d}" for y in years for d in days]
    datetimes = [datetime.date(*[int(j) for j in i.split('-')]) for i in dates_strs]
    for language in languages:
        update_propers_for_dates(
            datetimes,
            language,
            os.path.join(HERE, "fixtures", f"propers_{language}.json")
        )