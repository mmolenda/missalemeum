import unittest
from missal1962.missal import Missal
from datetime import datetime
import json


class TestMissal(unittest.TestCase):

    def _to_date_obj(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date()

    def test_missal(self):
        with open('vardays_fixtures.json') as fh:
            expected = json.load(fh)

        for year, dates in sorted(expected.iteritems()):
            missal = Missal(int(year))
            self.assertEqual(self._to_date_obj(dates[0]), missal.get_day_by_id('dom_septuagesima')[0])
            self.assertEqual(self._to_date_obj(dates[1]), missal.get_day_by_id('f4_cinerum')[0])
            self.assertEqual(self._to_date_obj(dates[2]), missal.get_day_by_id('DOM_RESSURECTIONIS')[0])
            self.assertEqual(self._to_date_obj(dates[3]), missal.get_day_by_id('ascensione_domini')[0])
            self.assertEqual(self._to_date_obj(dates[4]), missal.get_day_by_id('pentecost')[0])
            self.assertEqual(self._to_date_obj(dates[5]), missal.get_day_by_id('corporis_christi')[0])
            self.assertEqual(self._to_date_obj(dates[6]), missal.get_day_by_id('dom_adventus_1')[0])

if __name__ == '__main__':
    unittest.main()