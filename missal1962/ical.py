import datetime

from icalendar import Calendar, Event
from typing import Dict

from kalendar.models import Day


class IcalBuilder:

    @staticmethod
    def build(days: Dict[datetime.date, Day], rank: int, lang: str) -> str:
        cal = Calendar()
        cal.add('version', '2.0')
        cal.add("prodid", "-//Missale Meum - Calendar//missalemeum.com//")
        for datetime_, day in days.items():
            celebration = day.celebration[0] if day.celebration else day.tempora[0] if day.tempora else None
            if celebration is None or celebration.rank > rank:
                continue
            now = datetime.datetime.utcnow()
            event = Event()
            event.add("summary", celebration.title)
            event.add("dtstart", datetime_)
            event.add("dtstamp", now)
            event.add("uid", f"{datetime_.strftime('%Y%m%d')}@missalemeum.com")

            # Map color arrau to an array of human readable strings
            color_map = {
              "w": "white",
              "r": "red",
              "b": "black",
              "v" : "violet",
              "g" : "green",
            }

            colors = []
            for c in celebration.colors:
                colors.append(color_map[c])

            # Map ranks to human readable strings
            rank_map = {
              1: "First Class Feast",
              2: "Second Class Feast",
              3: "Third Class Feast",
              4 : "Feria",
            }

            rank_str = rank_map[celebration.rank]

            # description  = "Rank: " + str(celebration.rank) + '\n'
            description  = rank_str + '\n'

            if len(colors) == 1:
                description += "Vestment color: " + ", ".join(colors) + '\n'
            elif len(colors) > 1:
                description += "Vestment colors: " + ", ".join(colors) + '\n'

            description += "\n"
            description += "Propers: https://www.missalemeum.com/{}/{}".format(lang, datetime_.strftime("%Y-%m-%d")) + "\n"

            event.add("description", description)
            cal.add_component(event)
        return cal.to_ical().decode("utf-8")

