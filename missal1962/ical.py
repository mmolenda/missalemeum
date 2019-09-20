import datetime
from icalendar import Calendar, Event
from typing import Dict

from kalendar.models import Day


class IcalBuilder:

    @staticmethod
    def build(days: Dict[datetime.date, Day]) -> str:
        cal = Calendar()

        for datetime_, day in days.items():

            if len(day.celebration) < 1:
                continue
            celebration = day.celebration[0]
            if celebration.rank > 2:
                continue
            event = Event()
            event.add('summary', celebration.title)
            event.add('dtstart', datetime_)
            cal.add_component(event)

        return cal.to_ical().decode("utf-8")
