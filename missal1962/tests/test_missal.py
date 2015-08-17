
import json
import unittest
from datetime import datetime, date

from missal1962.constants import *
from missal1962.missal import Missal, MissalFactory
from missal1962.models import LiturgicalDay


class TestMissal(unittest.TestCase):

    def _to_date_obj(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

    def test_vardays(self):
        with open('vardays_fixtures.json') as fh:
            expected = json.load(fh)

        for year, dates in sorted(expected.iteritems()):
            missal = MissalFactory.create(int(year))
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

    def test_semi_fixed_days_all_souls(self):
        missal = MissalFactory.create(2008)
        self.assertEqual(date(2008, 11, 3), missal.get_day_by_id(FIX_11_02_OMNIUM_FIDELIUM_DEFUNCTORUM)[0])
        missal = MissalFactory.create(2014)
        self.assertEqual(date(2014, 11, 3), missal.get_day_by_id(FIX_11_02_OMNIUM_FIDELIUM_DEFUNCTORUM)[0])
        missal = MissalFactory.create(2015)
        self.assertEqual(date(2015, 11, 2), missal.get_day_by_id(FIX_11_02_OMNIUM_FIDELIUM_DEFUNCTORUM)[0])
        missal = MissalFactory.create(2063)
        self.assertEqual(date(2063, 11, 2), missal.get_day_by_id(FIX_11_02_OMNIUM_FIDELIUM_DEFUNCTORUM)[0])

    def test_semi_fixed_days_feb_24_related(self):
        missal = MissalFactory.create(2012)
        self.assertEqual(date(2012, 2, 25), missal.get_day_by_id(FIX_02_24_MATTHIAE_APOSTOLI)[0])
        self.assertEqual(date(2012, 2, 28), missal.get_day_by_id(FIX_02_27_1)[0])
        missal = MissalFactory.create(2016)
        self.assertEqual(date(2016, 2, 25), missal.get_day_by_id(FIX_02_24_MATTHIAE_APOSTOLI)[0])
        self.assertEqual(date(2016, 2, 28), missal.get_day_by_id(FIX_02_27_1)[0])
        missal = MissalFactory.create(2017)
        self.assertEqual(date(2017, 2, 24), missal.get_day_by_id(FIX_02_24_MATTHIAE_APOSTOLI)[0])
        self.assertEqual(date(2017, 2, 27), missal.get_day_by_id(FIX_02_27_1)[0])
        missal = MissalFactory.create(2018)
        self.assertEqual(date(2018, 2, 24), missal.get_day_by_id(FIX_02_24_MATTHIAE_APOSTOLI)[0])
        self.assertEqual(date(2018, 2, 27), missal.get_day_by_id(FIX_02_27_1)[0])

    def test_concurrency_12_08_conceptione_immaculata_bmv(self):
        self.assertEqual([FIX_12_08_CONCEPTIONE_IMMACULATA_BMV, VAR_DOM_ADVENTUS_2],
                         [i.id for i in MissalFactory.create(1907)[date(1907, 12, 8)]])
        self.assertEqual([FIX_12_08_CONCEPTIONE_IMMACULATA_BMV, VAR_DOM_ADVENTUS_2],
                         [i.id for i in MissalFactory.create(1912)[date(1912, 12, 8)]])
        self.assertEqual([FIX_12_08_CONCEPTIONE_IMMACULATA_BMV, VAR_F2_ADVENTUS_2],
                         [i.id for i in MissalFactory.create(1913)[date(1913, 12, 8)]])

    def test_concurrency_1_2_class_feast_of_the_Lord_occurring_on_sunday_2_class(self):
        self.assertEqual([FIX_01_06_EPIPHANIA],
                         [i.id for i in MissalFactory.create(2013)[date(2013, 1, 6)]])
        self.assertEqual([FIX_01_06_EPIPHANIA],
                         [i.id for i in MissalFactory.create(2036)[date(2036, 1, 6)]])

        self.assertEqual([VAR_DOM_SANCTAE_FAMILIAE],
                         [i.id for i in MissalFactory.create(2013)[date(2013, 1, 13)]])
        self.assertEqual([VAR_DOM_SANCTAE_FAMILIAE],
                         [i.id for i in MissalFactory.create(2036)[date(2036, 1, 13)]])

        self.assertEqual([FIX_08_06_TRANSFIGURATIONE],
                         [i.id for i in MissalFactory.create(1911)[date(1911, 8, 6)]])
        self.assertEqual([FIX_08_06_TRANSFIGURATIONE],
                         [i.id for i in MissalFactory.create(1922)[date(1922, 8, 6)]])

    def test_concurrency_vigil_nativitatis(self):
        self.assertEqual([FIX_12_24_VIGILIA_NATIVITATIS_DOMINI],
                         [i.id for i in MissalFactory.create(1950)[date(1950, 12, 24)]])
        self.assertEqual([FIX_12_24_VIGILIA_NATIVITATIS_DOMINI],
                         [i.id for i in MissalFactory.create(2000)[date(2000, 12, 24)]])

    def test_liturgical_day_model_simple_case(self):
        self.assertEqual(LiturgicalDay(VAR_F4_POST_EPIPHANIA_2, date(2002, 1, 23)).rank, 4)
        self.assertEqual(LiturgicalDay(VAR_F4_POST_EPIPHANIA_2, date(2002, 1, 23)).weekday, 2)
        self.assertEqual(LiturgicalDay(VAR_DOM_SEPTUAGESIMA, date(2002, 1, 27)).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_DOM_SEPTUAGESIMA, date(2002, 1, 27)).weekday, 6)
        self.assertEqual(LiturgicalDay(VAR_DOM_SEPTUAGESIMA, date(2002, 1, 28)).weekday, 6)

    def test_liturgical_day_model_variable_rank_advent(self):
        # 2002
        self.assertEqual(LiturgicalDay(VAR_F2_ADVENTUS_3, date(2015, 12, 16)).rank, 3)
        self.assertEqual(LiturgicalDay(VAR_F3_ADVENTUS_3, date(2015, 12, 17)).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_F4_QUATTUOR_ADVENTUS, date(2015, 12, 18)).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_F5_ADVENTUS_3, date(2015, 12, 19)).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_F6_QUATTUOR_ADVENTUS, date(2015, 12, 20)).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_SAB_QUATTUOR_ADVENTUS, date(2015, 12, 21)).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_DOM_ADVENTUS_4, date(2015, 12, 22)).rank, 1)
        self.assertEqual(LiturgicalDay(VAR_F2_ADVENTUS_4, date(2015, 12, 23)).rank, 2)
        # 2015
        self.assertEqual(LiturgicalDay(VAR_F3_ADVENTUS_3, date(2015, 12, 15)).rank, 3)
        self.assertEqual(LiturgicalDay(VAR_F4_QUATTUOR_ADVENTUS, date(2015, 12, 16)).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_F5_ADVENTUS_3, date(2015, 12, 17)).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_F6_QUATTUOR_ADVENTUS, date(2015, 12, 18)).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_SAB_QUATTUOR_ADVENTUS, date(2015, 12, 19)).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_DOM_ADVENTUS_4, date(2015, 12, 20)).rank, 1)
        self.assertEqual(LiturgicalDay(VAR_F2_ADVENTUS_4, date(2015, 12, 21)).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_F3_ADVENTUS_4, date(2015, 12, 22)).rank, 2)
        self.assertEqual(LiturgicalDay(VAR_F4_ADVENTUS_4, date(2015, 12, 23)).rank, 2)

    def test_liturgical_day_compare(self):
        rank_1_1 = LiturgicalDay(VAR_PENTECOST, date(2015, 5, 24))
        rank_1_2 = LiturgicalDay(FIX_11_01_OMNIUM_SANCTORUM, date(2015, 11, 1))
        rank_2_1 = LiturgicalDay(VAR_DOM_SANCTAE_FAMILIAE, date(2015, 1, 11))
        rank_2_2 = LiturgicalDay(FIX_01_13_BAPTISMATIS_DOMINI, date(2015, 1, 13))
        rank_3_1 = LiturgicalDay(VAR_F6_PASSIONIS, date(2015, 3, 27))
        rank_3_2 = LiturgicalDay(FIX_03_28_1, date(2015, 3, 28))
        rank_4_1 = LiturgicalDay(VAR_F2_POST_PENTECOST_1, date(2015, 6, 1))
        rank_4_2 = LiturgicalDay(FIX_08_09_2, date(2015, 8, 9))

        self.assertEqual(rank_1_1, rank_1_2)
        self.assertGreaterEqual(rank_1_1, rank_1_2)
        self.assertLessEqual(rank_1_1, rank_1_2)
        self.assertNotEqual(rank_1_1, rank_2_1)
        self.assertGreater(rank_1_1, rank_2_1)
        self.assertGreater(rank_1_1, rank_3_1)
        self.assertGreater(rank_1_1, rank_4_1)

        self.assertLess(rank_2_1, rank_1_1)
        self.assertEqual(rank_2_1, rank_2_2)
        self.assertGreaterEqual(rank_2_1, rank_2_2)
        self.assertLessEqual(rank_2_1, rank_2_2)
        self.assertNotEqual(rank_2_1, rank_3_2)
        self.assertGreater(rank_2_1, rank_3_1)
        self.assertGreater(rank_2_1, rank_4_1)

        self.assertLess(rank_3_1, rank_1_1)
        self.assertLess(rank_3_1, rank_2_1)
        self.assertEqual(rank_3_1, rank_3_2)
        self.assertGreaterEqual(rank_3_1, rank_3_2)
        self.assertLessEqual(rank_3_1, rank_3_2)
        self.assertNotEqual(rank_3_1, rank_4_1)
        self.assertGreater(rank_3_1, rank_4_1)

        self.assertLess(rank_4_1, rank_1_1)
        self.assertLess(rank_4_1, rank_2_1)
        self.assertLess(rank_4_1, rank_3_1)
        self.assertNotEqual(rank_4_1, rank_3_1)
        self.assertEqual(rank_4_1, rank_4_2)
        self.assertGreaterEqual(rank_4_1, rank_4_2)
        self.assertLessEqual(rank_4_1, rank_4_2)


if __name__ == '__main__':
    unittest.main()