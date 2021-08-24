import json
import logging
import os
import re
from typing import List, Union, Pattern

import mistune
import yaml

from constants.common import CUSTOM_PREFACES, PROPERS_DIR, SUPPLEMENT_DIR
from exceptions import SupplementNotFound, SectionNotFound

log = logging.getLogger(__name__)


def match(observances: Union[str, 'Observance', List[Union[str, 'Observance']]],  # noqa: F821
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


def get_custom_preface(celebration: 'Observance', tempora: 'Observance' = None) -> Union[str, None]:  # noqa: F821
    for pattern, preface_name in CUSTOM_PREFACES:
        if (re.match(pattern, celebration.id)) or (tempora and celebration.rank > 1 and re.match(pattern, tempora.id)):
            return preface_name
    return None


def format_day_propers(day: 'Day'):  # noqa: F821
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


def format_propers(propers):
    propers_vernacular, propers_latin = propers
    title = propers_vernacular.title
    info = {
        "title": title,
        "description": propers_vernacular.description,
        "additional_info": propers_vernacular.additional_info,
        "rank": propers_vernacular.rank,
        "colors": propers_vernacular.colors,
        "supplements": propers_vernacular.supplements,
    }
    return [{
        "info": info,
        "sections": format_proper_sections(propers_vernacular, propers_latin)
    }]


def format_proper_sections(propers_vernacular, propers_latin):
    pv = propers_vernacular.serialize()
    pl = {i["id"]: i["body"] for i in propers_latin.serialize()}
    result = []
    for section in pv:
        try:
            section["body"] = [[section["body"], pl[section["id"]]]]
        except KeyError:
            log.warning(f"Section `%s` not found in latin proper `%s`.", section['id'], propers_latin.id)
        else:
            result.append(section)
    return result


def get_pregenerated_proper(lang, proper_id):
    if not proper_id:
        return
    path = os.path.join(PROPERS_DIR, lang, f"{proper_id.replace(':', '__')}.json")
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
