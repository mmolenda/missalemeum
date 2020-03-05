import os
import re
from typing import List, Union, Pattern

import yaml

from constants.common import CUSTOM_PREFACES
from exceptions import SupplementNotFound


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
        try:
            if (re.match(pattern, celebration.id)) or (tempora and celebration.rank > 1 and re.match(pattern, tempora.id)):
                return preface_name
        except AttributeError:
            raise
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
            "color": propers_vernacular.color,
            "supplements": propers_vernacular.supplements,
            "date": day.date.strftime("%Y-%m-%d")
        }
        retvals.append({
            "info": info,
            "proper_vernacular": propers_vernacular.serialize(),
            "proper_latin": propers_latin.serialize()
        })
    return retvals


def get_supplement(root_path, lang, resource, subdir=None):
    try:
        path_args = [root_path, "supplement", lang]
        if subdir:
            path_args.append(subdir)
        path_args.append(f"{resource}.yaml")
        with open(os.path.join(*path_args)) as fh:
            return yaml.load(fh)
    except IOError:
        raise SupplementNotFound(f"{subdir}/{resource}")
