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
            description  = "Rank: " + str(celebration.rank) + '\n'

            # TODO : convert r,w,etc to red, white, etc
            description += "Color: " + str(celebration.colors.join(", ")) + '\n'

            # TODO : add option to add propers here
            # TODO : always add introit
            description += "Full propers: https://www.missalemeum.com/{}/{}".format(lang, datetime_.strftime("%Y-%m-%d")) + "\n"
            #print(dir(celebration.get_proper))
            #print(dir(celebration.colors))
            #print(dir(celebration))
            event.add("description", description)
            cal.add_component(event)
        return cal.to_ical().decode("utf-8")

