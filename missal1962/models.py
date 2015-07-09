
import re
from missal1962.constants import *
from missal1962.rules import determine_rank

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

    def __init__(self, day_id, day):
        flexibility, name, rank = re.match(
            '([\w]+?)_([\w]+):([\d]+)', day_id).groups()
        self.id = day_id
        self.name = name
        self.rank = determine_rank(day_id, day)
        if flexibility == TYPE_VAR:
            self.weekday = self.WEEKDAY_MAPPING[name.split('_')[0]]
        else:
            self.weekday = day.weekday()

    def __repr__(self):
        return "<{}>".format(self.name) 
