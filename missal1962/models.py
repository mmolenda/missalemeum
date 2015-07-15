
import re
from missal1962.constants import *

pattern__advent_feria_17_23 = re.compile('var_[fs][^_]+_adventus')

VARIABLE_RANK_MAP = (
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 17, "rank": 2},
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 18, "rank": 2},
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 19, "rank": 2},
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 20, "rank": 2},
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 21, "rank": 2},
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 22, "rank": 2},
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 23, "rank": 2},
)

WEEKDAY_MAPPING = {
    'f2': 0,
    'f3': 1,
    'f4': 2,
    'f5': 3,
    'f6': 4,
    'sab': 5,
    'dom': 6
}

class LiturgicalDay(object):
    """
    A class representing single liturgical day.
    It parses day's ID and extracts weekday,
    day's class/rank and human readable identifier.

    Example:
        'var_f3_post_epiphania_2:2'
        rank: 2
        weekday: 1
        name = var_f3_post_epiphania_2
    """
    def __init__(self, day_id, day):
        flexibility, name, rank = re.match(
            '([\w]+?)_([\w]+):([\d]+)', day_id).groups()
        self.id = day_id
        self.flexibility = flexibility
        self.name = name
        self.rank = self._determine_rank(day_id, day)
        if flexibility == TYPE_VAR:
            self.weekday = WEEKDAY_MAPPING[name.split('_')[0]]
        else:
            self.weekday = day.weekday()

    def _determine_rank(self, day_id, day):
        """
        Some liturgical days' ranks depend on calendar day
        a liturgay occur, for example:
          Advent feria days between 17 and 23 December are 2 class,
          while other feria Advent days are 3 class;
        """
        for case in VARIABLE_RANK_MAP:
            if re.match(case['pattern'], day_id) \
                    and day.month == case['month'] \
                    and day.day == case['day']:
                return case['rank']
        return int(day_id.split(':')[1])

    def __repr__(self):
        return "<{}>".format(self.id)

    def __eq__(self, other):
        return not self.rank < other.rank and not other.rank < self.rank

    def __ne__(self, other):
        return self.rank < other.rank or other.rank < self.rank

    def __ge__(self, other):
        return not self.rank < other.rank

    def __gt__(self, other):
        return other.rank > self.rank

    def __lt__(self, other):
        return other.rank < self.rank

    def __le__(self, other):
        return not other.rank > self.rank
