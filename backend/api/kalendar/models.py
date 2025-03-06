import datetime
import importlib
import logging
import re
from collections import OrderedDict
from copy import copy
from datetime import date, timedelta
from typing import ItemsView, List, Tuple, Union

from api.constants.common import (TEMPORA_C_10A, TEMPORA_C_10B, TEMPORA_C_10C, TEMPORA_C_10PASC, TEMPORA_C_10T,
                              TABLE_OF_PRECEDENCE, TEMPORA_EPI1_0,
                              TEMPORA_EPI1_0A, TEMPORA_PENT01_0,
                              TEMPORA_RANK_MAP, TYPE_TEMPORA, WEEKDAY_MAPPING, PATTERN_EASTER,
                              PATTERN_PRE_LENTEN,
                              PATTERN_LENT, GRADUALE_PASCHAL, TRACTUS, GRADUALE,
                              CUSTOM_INTER_READING_SECTIONS,
                              SUNDAY, PATTERN_POST_EPIPHANY_SUNDAY, TEMPORA_PENT23_0, INTROIT, OFFERTORIUM,
                              COMMUNIO,
                              TEMPORA_NAT2_0, SANCTI_01_01, PREFATIO_COMMUNIS, TEMPORA_PASC5_0,
                              TEMPORA_PASC5_4,
                              TEMPORA_PENT01_0A, FERIA)
from api.propers.models import Proper, ProperConfig
from api.propers.parser import ProperParser
from api.utils import get_custom_preface, match_first

log = logging.getLogger(__name__)


class Observance:
    """
    A class representing a single observance, such as "The first Friday after Pentecost" or "Assumption of Mary".
    It parses observance's ID and extracts weekday, day's class/rank, human readable identifier and vestment color.

    Example:
      'tempora:Epi2-4:4:g'
      rank: 4
      weekday: 3
      name: Epi2-4
      color: green

    Each identifier consists of four colon-separated elements:
      flexibility - determines if it's a fixed (sancti) or movable (tempora) observance
      identifier - a unique human readable observance identifier. In case of movable
        days it's a day's name, in case of 'sancti' days it contains a date
        in format %m-%d
      rank - observance's class, a number between 1 and 4
      vestment color - a string consisting of one ore more concatenated first letters of vestment color

    Example:
      'tempora:Epi2-3:4:g' - means movable day of fourth class
        which is third feria day (Wednesday) in second week after Epiphany, vestment color is green
      'sancti:11-19:4:w' - means a fixed day of fourth class falling on 19 Nov, color is white
    """
    def __init__(self, observance_id: str, date_: date, lang: str):
        """ Build an Observance out of identifier and calendar date

        :param observance_id: observance's identifier in format
                       <flexibility>:<identifier>:<rank>
        :type observance_id: string
        :param date_: specific date in which the observance is supposed
                    to be placed. For some Sancti days its rank (class)
                    depends on which calendar day they occur.
        :type date_: `date ` object
        """
        self.date = date_
        self.lang = lang
        translation = importlib.import_module(f'constants.{lang}.translation')
        flexibility, name, rank, color = observance_id.split(':')
        self.flexibility: str = flexibility
        self.name: str = name
        self.rank: int = self._calc_rank(observance_id, int(rank))
        self.colors = list(color)
        self.id: str = ':'.join((self.flexibility, self.name, str(self.rank), color))
        self.title: str = translation.TITLES.get(observance_id)
        if flexibility == TYPE_TEMPORA and observance_id not in (TEMPORA_C_10A, TEMPORA_C_10B, TEMPORA_C_10C, TEMPORA_C_10PASC, TEMPORA_C_10T):
            self.weekday = WEEKDAY_MAPPING[re.sub(r'^.*-(\d+).*$', '\\1', name)]
        else:
            self.weekday = self.date.weekday()
        self.priority = self._calc_priority()

    def get_proper(self, config=None) -> Tuple['Proper', 'Proper']:
        proper: Tuple['Proper', 'Proper'] = ProperParser(self.id, self.lang, config).parse()
        if re.match(PATTERN_POST_EPIPHANY_SUNDAY, self.id) and self.date.month >= 10:
            self._adjust_sunday_shifted_from_post_epiphany(proper)
        return proper

    def has_proper(self) -> bool:
        return ProperParser(self.id, self.lang).proper_exists()

    def serialize(self) -> dict:
        return {'id': self.id, 'rank': self.rank, 'title': self.title, 'colors': self.colors}

    def _calc_rank(self, observance_id: str, original_rank: int) -> int:
        """
        Some observance's ranks depend on calendar day on which they fall, for example:
          Advent feria days between 17 and 23 December are 2 class,
          while other feria Advent days are 3 class;
        """
        for case in TEMPORA_RANK_MAP:
            if self.date.month == case['month']\
                    and self.date.day == case['day']\
                    and re.match(case['pattern'], observance_id):
                return case['rank']
        return original_rank

    def _calc_priority(self) -> Union[None, int]:
        """
        Calculate priority according to the Precedence Table.
        """
        for priority, pattern in enumerate(TABLE_OF_PRECEDENCE):
            if re.match(pattern, self.id):
                return priority

    def _adjust_sunday_shifted_from_post_epiphany(self, propers: Tuple['Proper', 'Proper']) \
            -> Tuple['Proper', 'Proper']:
        """
        When Easter is early (e.g. 2018), Pre-lent takes up some Sundays after Epiphany, which in turn
        are shifted to the end of the period after Pentecost. In such case, each shifted Sunday is modified
        in following way:
          * Introit, Gradual, Offertorium and Communio are taken from 23rd Sunday after Pentecost
          * Collect, Lectio, Evangelium and Secreta are taken from respective shifted Sunday
        """
        proper_sunday_23_post_pentecost: Tuple['Proper', 'Proper'] = ProperParser(TEMPORA_PENT23_0, self.lang).parse()
        for i, proper in enumerate(propers):
            for section in (INTROIT, GRADUALE, OFFERTORIUM, COMMUNIO):
                proper.set_section(section, proper_sunday_23_post_pentecost[i].get_section(section))

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


class Day:
    """ Class used to keep `Observance` objects for particular days of Missal.

    It contains three lists: `tempora`, `celebration` and `commemoration`.
    On Missal's creation the lists are filled in so that `tempora` always contains `Observance` representing
    given variable day, `celebration` contains an `Observance`s to be celebrated in this day and
    `commemoration` contains zero or more `Observance`s that should be commemorated with the main celebration.
    """
    def __init__(self, date_: date, calendar: 'Calendar') -> None:
        self.date = date_
        self.calendar: 'Calendar' = calendar
        self.tempora: List['Observance'] = []
        self.celebration: List['Observance'] = []
        self.commemoration: List['Observance'] = []

    @property
    def all(self) -> List['Observance']:
        return self.tempora + self.celebration + self.commemoration

    def get_tempora_id(self) -> Union[None, str]:
        if self.tempora:
            return self.tempora[0].id

    def get_tempora_name(self) -> Union[None, str]:
        if self.tempora:
            return self.tempora[0].title

    def get_celebration_id(self) -> Union[None, str]:
        if self.celebration:
            return self.celebration[0].id

    def get_celebration_name(self) -> Union[None, str]:
        if self.celebration:
            return self.celebration[0].title

    def get_commemorations_titles(self) -> List[str]:
        return [i.title for i in self.commemoration if i.id != self.get_celebration_id()]

    def get_celebration_colors(self) -> Union[None, List[str]]:
        if self.celebration:
            return self.celebration[0].colors
    def get_celebration_rank(self) -> Union[None, int]:
        if self.celebration:
            return self.celebration[0].rank

    def get_proper(self) -> List[Tuple['Proper', 'Proper']]:
        """
        Get proper that is used in today Mass. If given day does not have a dedicated proper,
        use the one from the latest Sunday.
        """
        log.debug("Getting proper for day %s", self)
        celebration_propers = self._calculate_proper(self.celebration)
        if self.commemoration:
            commemoration_propers = self._calculate_proper(self.commemoration)
            for celebration_proper in celebration_propers:
                for i in {0: "vernacular", 1: "latin"}.keys():
                    proper = celebration_proper[i]
                    commemorations = [cp[i] for cp in commemoration_propers if proper.id != cp[i].id]
                    proper.add_commemorations(commemorations)
        return celebration_propers

    def _calculate_proper(self, observances: List[Observance]) -> List[Tuple['Proper', 'Proper']]:
        """
        Accommodate propers for given observance to the current calendar day.
        For example:
         * In paschal time show paschal gradual instead of regular gradual
         * In Lent show tractus instead of gradual
         * In feria days, when the proper from the last sunday is used, adjust day's class, remove "alleluja", etc.
         * In Sundays after Epiphany moved to the period after Pentecost adjust the sections accordingly
         * Show proper prefatio
         * etc.
        """
        if observances and all([i.has_proper() for i in observances]):
            retval: List[Tuple[Proper, Proper]] = []
            for observance in observances:
                inter_readings_section = self._infer_inter_reading_section(observance)
                preface = get_custom_preface(observance, next(iter(self.tempora), None))
                proper_config = ProperConfig(preface=preface, inter_readings_section=inter_readings_section)
                retval.append(observance.get_proper(proper_config))
            return retval
        else:
            # It's a feria day without its own proper for which the last Sunday's proper is used
            inferred_observances = self._infer_observance()
            if observances and not match_first(observances, FERIA):
                rank: int = observances[0].rank
                preface: str = get_custom_preface(observances[0])
            else:
                rank: int = 4
                preface: str = get_custom_preface(inferred_observances)
            preface = preface if preface is not None else PREFATIO_COMMUNIS
            title_id = observances[0].id if observances else None
            config: ProperConfig = ProperConfig(title_id=title_id, preface=preface,
                                                strip_alleluia=True, strip_tract=True)
            propers: Tuple[Proper, Proper] = inferred_observances.get_proper(config)
            for proper in propers:
                proper.rank = rank
            return [propers]

    def _infer_observance(self) -> Observance:
        # No proper for this day, trying to get one from the latest Sunday or from the Epiphany
        date_: date = copy(self.date)
        while not (date_.weekday() == SUNDAY) and not (date_.month == 1 and date_.day == 6):
            if date_ == datetime.date(self.date.year, 1, 1):
                break
            date_ = date_ - datetime.timedelta(days=1)
        day: Day = self.calendar.get_day(date_)
        # Handling exceptions
        if day.celebration[0].id == TEMPORA_EPI1_0:
            # "Feast of the Holy Family" replaces "First Sunday after Epiphany"; use the latter in
            # following days without the own proper
            return Observance(TEMPORA_EPI1_0A, date_, self.calendar.lang)
        if day.celebration[0].id == TEMPORA_PENT01_0:
            # "Trinity Sunday" replaces "1st Sunday after Pentecost"; use the latter in
            # following days without the own proper
            return Observance(TEMPORA_PENT01_0A, date_, self.calendar.lang)
        if day.celebration[0].id == TEMPORA_NAT2_0:
            # When the last Sunday is the feast of Holy Name, use proper from Octave of the Nativity
            return Observance(SANCTI_01_01, date_, self.calendar.lang)
        if day.tempora:
            return day.tempora[0]
        return day.celebration[0]

    def _infer_inter_reading_section(self, observance):
        if observance.id in CUSTOM_INTER_READING_SECTIONS:
            return CUSTOM_INTER_READING_SECTIONS[observance.id]
        elif match_first(self.tempora, PATTERN_EASTER):
            return GRADUALE_PASCHAL
        elif match_first(self.tempora, [PATTERN_PRE_LENTEN, PATTERN_LENT]):
            return TRACTUS
        return GRADUALE

    def serialize(self) -> dict:
        serialized = {}
        for container in ('tempora', 'celebration', 'commemoration'):
            serialized[container] = [i.serialize() for i in getattr(self, container)]
        return serialized

    def __str__(self):
        return str(self.tempora) + str(self.celebration) + str(self.commemoration)


class Calendar:
    """
    Class representing a Calendar.

    Internally it keeps the data in an ordered dict of `Days`s where each key is a `date` object and value
    is a `Day` containing `Observance` objects organized inside Day's members. Example:

    {
      ...
      datetime.date(2008, 5, 3): Day(tempora:[Observance<tempora:Pasc5-6:4>]
                                     celebration:[Observance<sancti:05-03-1:1>],
                                     commemoration:[])
      datetime.date(2008, 5, 4): Day(tempora:[Observance<tempora:Pasc6-0:2>],
                                     celebration:[Observance<sancti:05-04-1:3>]
                                     commemoration:[])
      datetime.date(2008, 5, 5): Day(tempora:[Observance<tempora:Pasc6-1:4>],
                                     celebration:[Observance<sancti:05-05-1:3>]
                                     commemoration:[])
      datetime.date(2008, 5, 6): Day(tempora:[Observance<tempora:Pasc6-2:4>],
                                     celebration:[Observance<tempora:Pasc6-2:4>]
                                     commemoration:[])
      ...
    }
    """
    def __init__(self, year: int, lang: str) -> None:
        """ Build a calendar and fill it in with empty `Day` objects
        """
        self.lang = lang
        self._container = OrderedDict()
        self._build_empty_calendar(year)

    def _build_empty_calendar(self, year: int) -> None:
        date_ = date(year, 1, 1)
        while date_.year == year:
            self._container[date_] = Day(date_, self)
            date_ += timedelta(days=1)

    def get_day(self, date_: datetime.date) -> Day:
        return self._container.get(date_)

    def find_day(self, observance_id: str) -> Union[None, Tuple[date, Day]]:
        """ Return a day representation by observance ID, if any

        :param observance_id: observance's identifier, for example TEMPORA_EPI6_0
        :type observance_id: string
        :return: day representation
        :rtype: list(datetime, list)
        """
        for date_, day in self._container.items():
            if observance_id in [ii.id for ii in day.all]:
                return date_, day

    def items(self) -> ItemsView[date, Day]:
        return self._container.items()

    def serialize(self) -> dict:
        serialized = {}
        for date_, day in self.items():
            serialized[date_.strftime('%Y-%m-%d')] = day.serialize()
        return serialized
