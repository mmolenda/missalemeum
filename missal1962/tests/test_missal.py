import unittest
from missal1962.missal import Missal
from datetime import datetime


class TestMissal(unittest.TestCase):

    def _to_date_obj(self, date_str):
        return datetime.strptime(date_str, '%Y.%m.%d').date()

    def test_missal(self):
        expected = (
            ('2004.2.8',  '2004.2.25', '2004.4.11', '2004.5.20', '2004.5.30', '2004.6.10', '2004.11.28', 25),
            ('2005.1.23', '2005.2.9', '2005.3.27', '2005.5.5', '2005.5.15', '2005.5.26', '2005.11.27', 27),
        )
        missal = Missal(2004)
        self.assertEqual(self._to_date_obj(expected[0][0]), missal.get_day_by_id('dom_septuagesima')[0])
        self.assertEqual(self._to_date_obj(expected[0][1]), missal.get_day_by_id('f4_cinerum')[0])
        self.assertEqual(self._to_date_obj(expected[0][2]), missal.get_day_by_id('DOM_RESSURECTIONIS')[0])
        self.assertEqual(self._to_date_obj(expected[0][3]), missal.get_day_by_id('ascensione_domini')[0])
        self.assertEqual(self._to_date_obj(expected[0][4]), missal.get_day_by_id('pentecost')[0])
        self.assertEqual(self._to_date_obj(expected[0][5]), missal.get_day_by_id('corporis_christi')[0])
        self.assertEqual(self._to_date_obj(expected[0][6]), missal.get_day_by_id('dom_adventus_1')[0])

        missal = Missal(2005)
        self.assertEqual(self._to_date_obj(expected[1][0]), missal.get_day_by_id('dom_septuagesima')[0])
        self.assertEqual(self._to_date_obj(expected[1][1]), missal.get_day_by_id('f4_cinerum')[0])
        self.assertEqual(self._to_date_obj(expected[1][2]), missal.get_day_by_id('DOM_RESSURECTIONIS')[0])
        self.assertEqual(self._to_date_obj(expected[1][3]), missal.get_day_by_id('ascensione_domini')[0])
        self.assertEqual(self._to_date_obj(expected[1][4]), missal.get_day_by_id('pentecost')[0])
        self.assertEqual(self._to_date_obj(expected[1][5]), missal.get_day_by_id('corporis_christi')[0])
        self.assertEqual(self._to_date_obj(expected[1][6]), missal.get_day_by_id('dom_adventus_1')[0])

if __name__ == '__main__':
    unittest.main()