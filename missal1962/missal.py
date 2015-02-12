"""
Missal 1962
"""

from datetime import date, datetime, timedelta
from dateutil.easter import easter
import sys
import constants


class Missal(list):

    def __init__(self, year):
        # build empty missal
        day = date(year, 1, 1)
        while day.year == year:
            self.append([day, []])
            day += timedelta(days=1)

        # fill in variable days
        self.insert_block(self.calc_varday__dom_sanctae_familiae(year),
                          constants.vardays__post_epiphania)

        self.insert_block(self.calc_varday__dom_septuagesima(year),
                          constants.vardays__pascha)

        self.insert_block(self.calc_varday__dom_adventus(year),
                          constants.vardays__advent)

        self.insert_block(self.calc_varday__sab_before_dom_adventus(year),
                          constants.vardays__post_epiphania,
                          reverse=True,
                          overwrite=False)

        # fill in fixed days
        for date_, contents in self:
            date_id = date_.strftime("%m-%d")
            days = list(set([ii for ii in constants.fixdays
                             if ii.startswith(date_id)]))
            contents.extend(days)


    def insert_block(self, start_date, block, reverse=False, overwrite=True):
        if reverse:
            block = reversed(block)
        day_index = self.get_date_index(start_date)
        for ii, day in enumerate(block):
            index = day_index + ii if not reverse else day_index - ii
            if self[index][1] and not overwrite:
                break
            self[index][1] = [day]


    def get_date_index(self, date_):
        for ii, day in enumerate(self):
            if day[0] == date_:
                return ii


    def calc_varday__dom_ressurectionis(self, year):
        """ Ressurection (Easter) Sunday
        """
        return easter(year)


    def calc_varday__dom_sanctae_familiae(self, year):
        """ Dominica Sanctae Familiae Jesu Mariae Joseph
        First Sunday after Epiphany (06 January)
        """
        epiphany = date(year, 1, 6)
        wd = epiphany.weekday() 
        delta = 6 - wd if wd < 6 else 7
        return epiphany + timedelta(days=delta)


    def calc_varday__dom_septuagesima(self, year):
        """ Dominica in Septuagesima
        First day of a Ressurection Sunday related block.
        It's 63 days before Ressurection.
        """
        return self.calc_varday__dom_ressurectionis(year) - timedelta(days=63)


    def calc_varday__dom_adventus(self, year):
        """ Dominica I Adventus
        Nov 27 (if it's Sunday) or closest Sunday
        """
        advent = date(year, 11, 27)
        wd = advent.weekday()
        if wd != 6:
            advent += timedelta(days=6-wd)
        return advent

    def calc_varday__sab_before_dom_adventus(self, year):
        """ Last Saturday before Dominica I Adventus
        """
        return self.calc_varday__dom_adventus(year) - timedelta(days=1)



if __name__ == '__main__':
    year = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.now().year
    missal = Missal(year)

    for ii in missal:
        print ii[0].strftime('%A'), ii
