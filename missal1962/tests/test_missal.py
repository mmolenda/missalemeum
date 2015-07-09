import unittest
from missal1962.constants import *
from missal1962.missal import Missal
from missal1962.models import LiturgicalDay
from datetime import datetime
import json


class TestMissal(unittest.TestCase):

    def _to_date_obj(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

    def test_vardays(self):
        with open('vardays_fixtures.json') as fh:
            expected = json.load(fh)

        for year, dates in sorted(expected.iteritems()):
            missal = Missal(int(year))
            self.assertEqual(self._to_date_obj(dates[0]), missal.get_day_by_id(VAR_DOM_SEPTUAGESIMA)[0])
            self.assertEqual(self._to_date_obj(dates[1]), missal.get_day_by_id(VAR_F4_CINERUM)[0])
            self.assertEqual(self._to_date_obj(dates[2]), missal.get_day_by_id(VAR_DOM_RESURRECTIONIS)[0])
            self.assertEqual(self._to_date_obj(dates[3]), missal.get_day_by_id(VAR_ASCENSIONE_DOMINI)[0])
            self.assertEqual(self._to_date_obj(dates[4]), missal.get_day_by_id(VAR_PENTECOST)[0])
            self.assertEqual(self._to_date_obj(dates[5]), missal.get_day_by_id(VAR_CORPORIS_CHRISTI)[0])
            self.assertEqual(self._to_date_obj(dates[6]), missal.get_day_by_id(VAR_DOM_ADVENTUS_1)[0])
            # dom_post_epiphania_4 might not exist in given year, then None is returned
            actual = missal.get_day_by_id(VAR_DOM_POST_EPIPHANIA_4)[0] if \
                missal.get_day_by_id(VAR_DOM_POST_EPIPHANIA_4) else None
            self.assertEqual(self._to_date_obj(dates[7]), actual)
            self.assertEqual(self._to_date_obj(dates[8]), missal.get_day_by_id(VAR_SAB_QUATTUOR_SEPTEMBRIS)[0])
            self.assertEqual(self._to_date_obj(dates[9]), missal.get_day_by_id(VAR_SANCTISSIMI_NOMINIS_JESU)[0])
            self.assertEqual(self._to_date_obj(dates[10]), missal.get_day_by_id(VAR_JESU_CHRISTI_REGIS)[0])
            # dom_octavam_nativitatis might not exist in given year, then None is returned
            actual = missal.get_day_by_id(VAR_DOM_OCTAVAM_NATIVITATIS)[0] if \
                missal.get_day_by_id(VAR_DOM_OCTAVAM_NATIVITATIS) else None
            self.assertEqual(self._to_date_obj(dates[11]), actual)

    def test_liturgical_day_model(self):
        self.assertEqual(LiturgicalDay(VAR_DOM_SEPTUAGESIMA).rank, 1)
        self.assertEqual(LiturgicalDay(VAR_DOM_SEPTUAGESIMA).weekday, 6)
        self.assertEqual(LiturgicalDay(VAR_F4_POST_EPIPHANIA_4).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_F4_POST_EPIPHANIA_4).weekday, 2)


if __name__ == '__main__':
    unittest.main()