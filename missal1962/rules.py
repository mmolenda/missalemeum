# -*- coding: utf-8 -*-

"""
14. Niedzielę obchodzi się w jej własnym dniu, według rubryk. Nie odprawia
się wcześniej ani później Mszy i Oficjum niedzieli, która napotkała przeszkodę.

15. Niedziela I klasy w razie spotkania ma pierwszeństwo przed wszystkimi
świętami. Jednak święto Niepokalanego Poczęcia NMP ma pierwszeństwo przed
napotkaną niedzielą Adwentu.

16. Niedziela II klasy w razie zbieżności (occurentia) ma pierwszeństwo
przed świętami 2 klasy.
Jednak:

a) święto Pańskie 1 i 2 klasy przypadające w niedzielę 2 klasy zajmuje
miejsce niedzieli z wszystkimi prawami i przywilejami; dlatego nie wspomina
się niedzieli;
b) niedziela 2 klasy ma pierwszeństwo przed Dniem Zadusznym;

17. Zasadniczo na niedzielę nie wolno wyznaczać na stałe świąt.
Wyjątek stanowią:

a) święto Najświętszego Imienia Jezus, które obchodzi się w niedzielę przypadającą od 2 do 5 stycznia (lub 2 stycznia);
b) święto Świętej Rodziny Jezusa, Maryi i Józefa, które obchodzi się w pierwszą niedzielę po Objawieniu;
c) święto Najświętszej Trójcy, które obchodzi się w pierwszą niedzielę po Zesłaniu Ducha Świętego;
d) święto Chrystusa Króla, które obchodzi się w ostatnią niedzielę miesiąca października;
e) święta Pańskie 1 klasy, które obecnie wyznaczone są na niedziele 2 klasy w kalendarzach partykularnych;

Te święta zajmują miejsce przypadające niedzieli z wszystkimi prawami i przywilejami, dlatego nie wspomina się niedzieli.

"""
import re


pattern__advent_feria_17_23 = re.compile('var_[fs][^_]+_adventus')

VARIABLE_RANK_MAP = (
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 17, "rank": 2},
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 18, "rank": 2},
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 19, "rank": 2},
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 20, "rank": 2},
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 21, "rank": 2},
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 22, "rank": 2},
    {"pattern": pattern__advent_feria_17_23, "month": 12, "day": 23, "rank": 2},
)

def determine_rank(day_id, day):
    """
    Some liturgical days' ranks depend on calendar day
    a liturgay occur, for example:
      Advent feria days between 17 and 23 December are 2 class,
      while other feria Advent days are 3 class;
    """
    for case in VARIABLE_RANK_MAP:
        if re.match(case['pattern'], day_id) \
                and day.month == case['month'] \
                and day.day == case['day']:
            return case['rank']
    return int(day_id.split(':')[1])
