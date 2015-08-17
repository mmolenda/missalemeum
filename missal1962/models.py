from collections import OrderedDict
import re
from datetime import date, timedelta

from .constants import *

pattern__advent_feria_17_23 = re.compile('var:[fs][^_]+_adventus')

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


class Missal(OrderedDict):
    """ Class representing a Missal.

    It's an ordered dict of lists where each key is a `date` object and value
    is a list containing `LiturgicalDay` objects. Example:

    {
      ...
      datetime.date(2008, 5, 3): [<var:sab_post_ascension:4>,
                                  <fix:05-03.mariae_reginae_poloniae:1>],
      datetime.date(2008, 5, 4): [<var:dom_post_ascension:4>, <fix:05-04>],
      datetime.date(2008, 5, 5): [<var:f2_hebd_post_ascension:4>, <fix:05-05>],
      datetime.date(2008, 5, 6): [<var:f3_hebd_post_ascension:4>],
      ...
    }
    """
    def __init__(self, year):
        """ Build an empty missal and fill it in with liturgical days' objects
        """
        super(Missal, self).__init__()
        self._build_empty_missal(year)

    def _build_empty_missal(self, year):
        day = date(year, 1, 1)
        while day.year == year:
            self[day] = []
            day += timedelta(days=1)

    def get_day_by_id(self, day_id):
        """ Return a day representation by liturgical day ID

        :param dayid: liturgical days'identifier, for example
                      'var:f2_septuagesima:4'
        :type dayid: string
        :return: day representation
        :rtype: list(datetime, list)
        """
        for day in self.iteritems():
            if day_id in [ii.id for ii in day[1]]:
                return day


class LiturgicalDay(object):
    """
    A class representing single liturgical day.
    It parses day's ID and extracts weekday,
    day's class/rank and human readable identifier.

    Example:
      'var:f3_post_epiphania_2:2'
      rank: 2
      weekday: 1
      name = var:f3_post_epiphania_2

    Each identifier consists of three colon-separated elements:
      flexibility - determines if it's a fixed- (fix) or movable- (var)
        date liturgical day
      identifier - a unique human readable day identifier. In case of movable
        days it's a day's name, in case of fixed days it contains a date
        in format %m_%s and either consecutive number or human readable
        days name (in case of 1 and 2 class days, just for readability)
      rank - day's class, a number between 1 and 4

    Example:
      'var:f3_post_epiphania_2:2' - means movable day of second class
        which is third feria day in second week after Epiphany
      'fix:11_19_2:4' - means second fixed day of fourth class
        falling on 19 Nov
      'fix:12_26_stephani:2' - means fixed day of second class
         falling on 26 Dec, which happens to be st. Stephen's day
    """
    def __init__(self, day_id, day):
        """ Build a Liturgical day out of identifier and calendar date

        :param day_id: liturgical day identifier in format
                       <flexibility>:<identifier>:<rank>
        :type day_id: string
        :param day: specific date in which the liturgical day is supposed
                    to be placed. For some variable days its rank (class)
                    depends on which calendar day they occur
        :type day: `date ` object
        """
        flexibility, name, rank = day_id.split(':')
        self.flexibility = flexibility
        self.name = name
        self.rank = self._determine_rank(day_id, day, int(rank))
        self.id = ':'.join((self.flexibility, self.name, str(self.rank)))
        if flexibility == TYPE_VAR:
            self.weekday = WEEKDAY_MAPPING[name.split('_')[0]]
        else:
            self.weekday = day.weekday()

    def _determine_rank(self, day_id, day, original_rank):
        """
        Some liturgical days' ranks depend on calendar day
        they occur, for example:
          Advent feria days between 17 and 23 December are 2 class,
          while other feria Advent days are 3 class;
        """
        for case in VARIABLE_RANK_MAP:
            if day.month == case['month'] and day.day == case['day'] \
                    and re.match(case['pattern'], day_id):
                return case['rank']
        return original_rank

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
