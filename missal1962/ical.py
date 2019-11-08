import datetime
from icalendar import Calendar, Event
from typing import Dict

from kalendar.models import Day


class IcalBuilder:

    @staticmethod
    def build(days: Dict[datetime.date, Day], rank: int) -> str:
        cal = Calendar()
        cal.add('version', '2.0')
        cal.add("prodid", "-//Mszał Rzymski - Kalendarz//mszalrzymski.pl//")
        for datetime_, day in days.items():
            if len(day.celebration) < 1:
                continue
            celebration = day.celebration[0]
            if celebration.rank > rank:
                continue
            now = datetime.datetime.utcnow()
            event = Event()
            event.add("summary", celebration.title)
            event.add("dtstart", datetime_)
            event.add("dtstamp", now)
            event.add("uid", f"{datetime_.strftime('%Y%m%d')}@mszalrzymski.pl")
            event.add("description", "http://mszalrzymski.pl/#{}".format(datetime_.strftime("%Y-%m-%d")))
            cal.add_component(event)
        return cal.to_ical().decode("utf-8")
