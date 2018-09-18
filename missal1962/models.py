import re
from collections import OrderedDict
from datetime import date, timedelta
from typing import Tuple

from .blocks import TABLE_OF_PRECEDENCE
from .constants import TEMPORA_RANK_MAP, WEEKDAY_MAPPING, TYPE_TEMPORA
from .resources import titles_pl


class LiturgicalDayContainer(object):
    """ Class used to keep `LiturgicalDay` objects for particular days of Missal.

    It contains three lists: `tempora`, `celebration` and `commemoration`.
    On Missal's creation the lists are filled in so that `tempora` always contains `LiturgicalDay` representing
    given variable day, `celebration` contains a LiturgicalDay representing proper for this day's mass and
    `commemoration` contains zero or more `LiturgicalDays` that should be commemorated with the main proper.
    """
    tempora = None
    celebration = None
    commemoration = None

    def __init__(self):
        self.tempora = []
        self.celebration = []
        self.commemoration = []

    @property
    def all(self):
        return self.tempora + self.celebration + self.commemoration

    def __str__(self):
        return str(self.tempora) + str(self.celebration) + str(self.commemoration)


class Missal(OrderedDict):
    """ Class representing a Missal.

    It's an ordered dict of `LiturgicalDayContainer`s where each key is a `date` object and value
    is a `LiturgicalDayContainer` containing `LiturgicalDay` objects organized inside container's members. Example:

    {
      ...
      datetime.date(2008, 5, 3): LiturgicalDayContainer(tempora:[LiturgicalDay<tempora:Pasc5-6:4>]
                                                        celebration:[LiturgicalDay<sancti:05-03-1:1>],
                                                        commemoration:[])
      datetime.date(2008, 5, 4): LiturgicalDayContainer(tempora:[LiturgicalDay<tempora:Pasc6-0:2>],
                                                        celebration:[LiturgicalDay<sancti:05-04-1:3>]
                                                        commemoration:[])
      datetime.date(2008, 5, 5): LiturgicalDayContainer(tempora:[LiturgicalDay<tempora:Pasc6-1:4>],
                                                        celebration:[LiturgicalDay<sancti:05-05-1:3>]
                                                        commemoration:[])
      datetime.date(2008, 5, 6): LiturgicalDayContainer(tempora:[LiturgicalDay<tempora:Pasc6-2:4>],
                                                        celebration:[LiturgicalDay<tempora:Pasc6-2:4>]
                                                        commemoration:[])
      ...
    }
    """
    def __init__(self, year: int):
        """ Build a missal and fill it in with empty `LiturgicalDayContainer` objects
        """
        super(Missal, self).__init__()
        self._build_empty_missal(year)

    def _build_empty_missal(self, year: int):
        day = date(year, 1, 1)
        while day.year == year:
            self[day] = LiturgicalDayContainer()
            day += timedelta(days=1)

    def get_day(self, day_id: str) -> Tuple[date, LiturgicalDayContainer]:
        """ Return a day representation by liturgical day ID

        :param day_id: liturgical days'identifier, for example TEMPORA_EPI6_0
        :type day_id: string
        :return: day representation
        :rtype: list(datetime, list)
        """
        for day in self.items():
            if day_id in [ii.id for ii in day[1].all]:
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
      name: Epi2-4

    Each identifier consists of three colon-separated elements:
      flexibility - determines if it's a fixed (sancti) or movable (tempora) liturgical day
      identifier - a unique human readable day identifier. In case of movable
        days it's a day's name, in case of 'sancti' days it contains a date
        in format %m-%d
      rank - day's class, a number between 1 and 4

    Example:
      'tempora:Epi2-3:4' - means movable day of fourth class
        which is third feria day (Wednesday) in second week after Epiphany
      'sancti:11_19:4' - means a fixed day of fourth class falling on 19 Nov
    """
    def __init__(self, day_id: str, day: date):
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
        self.rank = self._calc_rank(day_id, day, int(rank))
        self.id = ':'.join((self.flexibility, self.name, str(self.rank)))
        self.title = titles_pl.titles.get(day_id)
        if flexibility == TYPE_TEMPORA:
            self.weekday = WEEKDAY_MAPPING[re.sub('^.*-(\d+).*$', '\\1', name)]
        else:
            self.weekday = day.weekday()
        self.priority = self._calc_priority()

    def _calc_rank(self, day_id: str, day: date, original_rank: int) -> int:
        """
        Some liturgical days' ranks depend on calendar day on which they fall, for example:
          Advent feria days between 17 and 23 December are 2 class,
          while other feria Advent days are 3 class;
        """
        for case in TEMPORA_RANK_MAP:
            if day.month == case['month'] and day.day == case['day'] and re.match(case['pattern'], day_id):
                return case['rank']
        return original_rank

    def _calc_priority(self) -> int:
        """
        Calculate priority according to the Precedence Table.
        """
        for priority, pattern in enumerate(TABLE_OF_PRECEDENCE):
            if re.match(pattern, self.id):
                return priority

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
