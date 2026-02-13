import datetime
from icalendar import Calendar, Event
from typing import Dict

from api.kalendar.models import Day


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
            now = datetime.datetime.now(datetime.UTC)
            event = Event()
            event.add("summary", celebration.title)
            event.add("dtstart", datetime_)
            event.add("dtstamp", now)
            event.add("uid", f"{datetime_.strftime('%Y%m%d')}@missalemeum.com")
            event.add("description", "https://www.missalemeum.com/{}/{}".format(lang, datetime_.strftime("%Y-%m-%d")))
            cal.add_component(event)
        return cal.to_ical().decode("utf-8")
