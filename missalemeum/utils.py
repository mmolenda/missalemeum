import json
import logging
import os
import re
from collections import defaultdict
from typing import List, Union, Pattern

import mistune
import yaml

from constants.common import CUSTOM_PREFACES, PROPERS_DIR, SUPPLEMENT_DIR, PATTERN_PRE_LENTEN, PATTERN_LENT, TRACTUS, \
    SANCTI_02_02, GRADUALE, SUPPLEMENT_DIR_V4
from exceptions import SupplementNotFound

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


def format_propers(propers, day=None):
    retvals = []
    for propers_vernacular, propers_latin in propers:
        title = propers_vernacular.title
        tempora_name: str = day.get_tempora_name() if day else None
        info = {
            "id": propers_vernacular.id,
            "title": title,
            "description": propers_vernacular.description,
            "additional_info": propers_vernacular.additional_info,
            "tempora": tempora_name if tempora_name != title else None,
            "rank": propers_vernacular.rank,
            "colors": propers_vernacular.colors,
            "supplements": propers_vernacular.supplements,
            "date": day.date.strftime("%Y-%m-%d") if day else None
        }
        retvals.append({
            "info": info,
            "sections": format_proper_sections(propers_vernacular, propers_latin)
        })
    return retvals


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


def get_pregenerated_proper(lang, proper_id, tempora_id=None):
    if not proper_id:
        return
    path = os.path.join(PROPERS_DIR, lang, f"{proper_id.replace(':', '__')}.json")
    if os.path.exists(path):
        with open(path) as fh:
            proper = json.load(fh)
            if proper_id == SANCTI_02_02 and tempora_id is not None:
                # Candlemass is the only pre-generated proper for which the gradual/tract differs
                # depending on liturgical period, hence this hack
                section_to_del = GRADUALE if match(tempora_id, [PATTERN_PRE_LENTEN, PATTERN_LENT]) else TRACTUS
                idx_to_del = [i for i, j in enumerate(proper[0]['sections']) if j['id'] == section_to_del][0]
                del proper[0]['sections'][idx_to_del]
            return proper


def get_supplement(lang, resource, subdir=None):
    try:
        path_args = [SUPPLEMENT_DIR, lang]
        if subdir:
            path_args.append(subdir)
        path_args.append(f"{resource}.yaml")
        with open(os.path.join(*path_args)) as fh:
            content = yaml.full_load(fh)
            content["body"] = mistune.markdown(content["body"], escape=False, plugins=['table'])
            return content
    except IOError:
        raise SupplementNotFound(f"{subdir}/{resource}")


def get_supplement_v4(lang, resource, subdir=None):
    try:
        path_args = [SUPPLEMENT_DIR_V4, lang]
        if subdir:
            path_args.append(subdir)
        path_args.append(f"{resource}.json")
        with open(os.path.join(*path_args)) as fh:
            content = json.load(fh)
            return content
    except IOError:
        raise SupplementNotFound(f"{subdir}/{resource}")


class SupplementIndex:
    CANTICUM = "canticum"
    ORATIO = "oratio"

    def __init__(self):
        self.index = defaultdict(list)

    def get_canticum_index(self, lang):
        return self._get_index(lang, self.CANTICUM)

    def get_canticum_title(self, lang, proper_id):
        return self._get_title(lang, self.CANTICUM, proper_id)

    def get_oratio_index(self, lang):
        return self._get_index(lang, self.ORATIO)

    def get_oratio_title(self, lang, proper_id):
        return self._get_title(lang, self.ORATIO, proper_id)

    def _get_index(self, lang, subdir):
        key = f"{lang}-{subdir}"
        if key not in self.index:
            try:
                filenames = os.listdir(os.path.join(SUPPLEMENT_DIR, lang, subdir))
            except FileNotFoundError:
                filenames = []
            finally:
                for filename in sorted(filenames):
                    if filename.endswith(".yaml"):
                        resource_id = filename.rsplit('.', 1)[0]
                        index_item = get_supplement(lang, resource_id, subdir)
                        self.index[key].append(
                            {"title": index_item["title"],
                             "ref": f"{subdir}/{resource_id}",
                             "tags": index_item["tags"]
                             })
        return self.index[key]

    def _get_title(self, lang, subdir, proper_id):
        for i in self._get_index(lang, subdir):
            if proper_id is not None and i["ref"].endswith(proper_id):
                return i["title"]


supplement_index = SupplementIndex()


class SupplementIndexV4(SupplementIndex):
    def _get_index(self, lang, subdir):
        key = f"{lang}-{subdir}"
        if key not in self.index:
            try:
                filenames = os.listdir(os.path.join(SUPPLEMENT_DIR_V4, lang, subdir))
            except FileNotFoundError:
                filenames = []
            finally:
                for filename in sorted(filenames):
                    if filename.endswith(".json"):
                        resource_id = filename.rsplit('.', 1)[0]
                        index_item = get_supplement_v4(lang, resource_id, subdir)
                        self.index[key].append(
                            {"title": index_item[0]["info"]["title"],
                             "id": resource_id,
                             "tags": index_item[0]["info"]["additional_info"]
                             })
        return self.index[key]


supplement_index_v4 = SupplementIndexV4()
