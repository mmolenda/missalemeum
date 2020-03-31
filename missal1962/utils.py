import json
import os
import re
from typing import List, Union, Pattern

import mistune
import yaml

from constants.common import CUSTOM_PREFACES, PROPERS_DIR, SUPPLEMENT_DIR
from exceptions import SupplementNotFound, SectionNotFound


def match(observances: Union[str, 'Observance', List[Union[str, 'Observance']]],
          patterns: Union[List[str], str, List[Pattern], Pattern]):
    if not isinstance(observances, (list, tuple)):
        observances = [observances]
    if not isinstance(patterns, (list, tuple)):
        patterns = [patterns]
    for observance in observances:
        observance_id = observance if isinstance(observance, str) else observance.id
        for pattern in patterns:
            if re.match(pattern, observance_id):
                return observance


def get_custom_preface(celebration: 'Observance', tempora: 'Observance' = None) -> Union[str, None]:
    for pattern, preface_name in CUSTOM_PREFACES:
        if (re.match(pattern, celebration.id)) or (tempora and celebration.rank > 1 and re.match(pattern, tempora.id)):
            return preface_name
    return None


def format_propers(day: 'Day'):
    propers = day.get_proper()
    retvals = []
    for propers_vernacular, propers_latin in propers:
        # In most of the cases calculate the celebration title from the Observance object falling on
        # a given day; in case of days with multiple masses (02 Nov, 25 Dec) get the title from
        # proper's comment directly
        title = day.get_celebration_name() if len(propers) < 2 else propers_vernacular.title
        tempora_name: str = day.get_tempora_name()
        info = {
            "id": day.get_celebration_id(),
            "title": title,
            "description": propers_vernacular.description,
            "additional_info": propers_vernacular.additional_info,
            "tempora": tempora_name if tempora_name != title else None,
            "rank": propers_vernacular.rank,
            "colors": propers_vernacular.colors,
            "supplements": propers_vernacular.supplements,
            "date": day.date.strftime("%Y-%m-%d")
        }
        retvals.append({
            "info": info,
            "sections": format_proper_sections(propers_vernacular, propers_latin)
        })
    return retvals


def format_proper_sections(propers_vernacular, propers_latin):
    pv = propers_vernacular.serialize()
    pl = {i["id"]: i["body"] for i in propers_latin.serialize()}
    for val in pv:
        try:
            val["body"] = [[val["body"], pl[val["id"]]]]
        except KeyError:
            raise SectionNotFound(f"Section `{val['id']}` not found in latin proper `{propers_latin.id}`.")
    return pv


def get_pregenerated_proper(lang, proper_id):
    path = os.path.join(PROPERS_DIR, lang, f"{proper_id}.json")
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)


def get_supplement(lang, resource, subdir=None):
    try:
        path_args = [SUPPLEMENT_DIR, lang]
        if subdir:
            path_args.append(subdir)
        path_args.append(f"{resource}.yaml")
        with open(os.path.join(*path_args)) as fh:
            content = yaml.full_load(fh)
            content["body"] = mistune.markdown(content["body"], escape=False)
            return content
    except IOError:
        raise SupplementNotFound(f"{subdir}/{resource}")
