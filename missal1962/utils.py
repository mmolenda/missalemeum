import re


def match(lit_days, patterns):
    if not isinstance(patterns, (list, tuple)):
        patterns = [patterns]
    for lit_day in lit_days:
        for pattern in patterns:
            if re.match(pattern, lit_day.id):
                return lit_day
