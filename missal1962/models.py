from collections import OrderedDict
import re
from datetime import date, timedelta

from constants import *

patterns = {
    'advent-sunday': re.compile(r'^tempora:Adv\d-0'),
    'advent-feria-between-17-and-23': re.compile('tempora:Adv\d-[1-6]'),
    'tempora-sunday-class-2': re.compile(r'^tempora:.*-0:2$'),
    'sancti-sunday-class-1-or-2': re.compile(r'^sancti:.*:[12]$')
}


TEMPORA_RANK_MAP = (
    {"pattern": patterns['advent-feria-between-17-and-23'], "month": 12, "day": 17, "rank": 2},
    {"pattern": patterns['advent-feria-between-17-and-23'], "month": 12, "day": 18, "rank": 2},
    {"pattern": patterns['advent-feria-between-17-and-23'], "month": 12, "day": 19, "rank": 2},
    {"pattern": patterns['advent-feria-between-17-and-23'], "month": 12, "day": 20, "rank": 2},
    {"pattern": patterns['advent-feria-between-17-and-23'], "month": 12, "day": 21, "rank": 2},
    {"pattern": patterns['advent-feria-between-17-and-23'], "month": 12, "day": 22, "rank": 2},
    {"pattern": patterns['advent-feria-between-17-and-23'], "month": 12, "day": 23, "rank": 2},
)

WEEKDAY_MAPPING = {
    '0': 6,
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5
}


class Missal(OrderedDict):
    """ Class representing a Missal.

    It's an ordered dict of lists where each key is a `date` object and value
    is a list containing `LiturgicalDay` objects. Example:

    {
      ...
      datetime.date(2008, 5, 3): [<tempora:Pasc5-6:4>,
                                  <sancti:05-03-1:1>],
      datetime.date(2008, 5, 4): [<tempora:Pasc6-0:2>, <sancti:05-04-1:3>],
      datetime.date(2008, 5, 5): [<tempora:Pasc6-1:4>, <sancti:05-05-1:3>],
      datetime.date(2008, 5, 6): [<tempora:Pasc6-2:4>],
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

        :param dayid: liturgical days'identifier, for example TEMPORA_EPI6_0
        :type dayid: string
        :return: day representation
        :rtype: list(datetime, list)
        """
        for day in self.items():
            if day_id in [ii.id for ii in day[1]]:
                return day


class LiturgicalDay(object):
    """
    A class representing single liturgical day.
    It parses day's ID and extracts weekday,
    day's class/rank and human readable identifier.

    Example:
      'tempora:Epi2-4:4'
      rank: 4
      weekday: 3
      name = Epi2-4

    Each identifier consists of three colon-separated elements:
      flexibility - determines if it's a fixed (sancti) or movable (tempora) liturgical day
      identifier - a unique human readable day identifier. In case of movable
        days it's a day's name, in case of 'sancti' days it contains a date
        in format %m-%d and a consecutive number
      rank - day's class, a number between 1 and 4

    Example:
      'tempora:Epi2-3:4' - means movable day of fourth class
        which is third feria day (Wednesday) in second week after Epiphany
      'sancti:11_19_2:4' - means second fixed day of fourth class
        falling on 19 Nov
    """
    def __init__(self, day_id, day):
        """ Build a Liturgical day out of identifier and calendar date

        :param day_id: liturgical day identifier in format
                       <flexibility>:<identifier>:<rank>
        :type day_id: string
        :param day: specific date in which the liturgical day is supposed
                    to be placed. For some Sancti days its rank (class)
                    depends on which calendar day they occur.
        :type day: `date ` object
        """
        flexibility, name, rank = day_id.split(':')
        self.flexibility = flexibility
        self.name = name
        self.rank = self._determine_rank(day_id, day, int(rank))
        self.id = ':'.join((self.flexibility, self.name, str(self.rank)))
        if flexibility == TYPE_TEMPORA:
            self.weekday = WEEKDAY_MAPPING[name.split('-')[-1]]
        else:
            self.weekday = day.weekday()

    def _determine_rank(self, day_id, day, original_rank):
        """
        Some liturgical days' ranks depend on calendar day on which they fall, for example:
          Advent feria days between 17 and 23 December are 2 class,
          while other feria Advent days are 3 class;
        """
        for case in TEMPORA_RANK_MAP:
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
