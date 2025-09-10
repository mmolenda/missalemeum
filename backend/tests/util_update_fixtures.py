import os
import datetime
import json
import os
import sys
from api.constants import common as const

from tests.conftest import get_missal, HERE
from tests.test_propers_local import days, years

def update_propers_for_dates(dates: list[datetime.date], language_and_section: str, fixture_path: str):
    tmpp = language_and_section.split("-")
    language = tmpp[0]
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

            if lookup_section := (tmpp[1] if len(tmpp) > 1 else None):
                with open(fixture_path, "r", encoding="utf-8") as fh:
                    existing_fixture = json.load(fh)
                coll[strdt][i] = []
                for j, section in enumerate(existing_fixture[strdt][i]):
                    to_append = {"id": srlzd[j]["id"], "body": srlzd[j]["body"][:120]} if lookup_section == srlzd[j]["id"] else section
                    coll[strdt][i].append(to_append)

            else:
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
            os.path.join(HERE, "fixtures", f"propers_{language.split("-")[0]}.json")
        )