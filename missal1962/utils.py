import re
from typing import List, Union


def match(observances: List['Observance'], patterns: Union[List[str], str]):
    if not isinstance(patterns, (list, tuple)):
        patterns = [patterns]
    for observance in observances:
        for pattern in patterns:
            if re.match(pattern, observance.id):
                return observance
