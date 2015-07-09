
import re
from missal1962.constants import *

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

    WEEKDAY_MAPPING = {
        'f2': 0,
        'f3': 1,
        'f4': 2,
        'f5': 3,
        'f6': 4,
        'sab': 5,
        'dom': 6
    }

    def __init__(self, day_id, weekday=None):
        flexibility, name, rank = re.match(
            '([\w]+?)_([\w]+):([\d]+)', day_id).groups()
        self.id = day_id
        self.name = name
        self.rank = int(rank)
        if flexibility == TYPE_VAR:
            self.weekday = self.WEEKDAY_MAPPING[name.split('_')[0]]
        else:
            self.weekday = None

    def __repr__(self):
        return "<{}>".format(self.name) 


