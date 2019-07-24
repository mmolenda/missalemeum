import re
from typing import List, Union

from constants.common import CUSTOM_PREFACES


def match(observances: List['Observance'], patterns: Union[List[str], str]):
    if not isinstance(patterns, (list, tuple)):
        patterns = [patterns]
    for observance in observances:
        for pattern in patterns:
            if re.match(pattern, observance.id):
                return observance


def infer_custom_preface(celebration: 'Observance', tempora: 'Observance' = None) -> Union[str, None]:
    for pattern, preface_name in CUSTOM_PREFACES:
        try:
            if (re.match(pattern, celebration.id)) or (tempora and celebration.rank > 1 and re.match(pattern, tempora.id)):
                return preface_name
        except AttributeError:
            raise
    return None
