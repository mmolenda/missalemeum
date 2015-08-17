
from datetime import date

def get_year_by_date_and_weekday(month, day, weekday):
    """
    Print years where certain date is on specific weekday
    """
    for year in range(1900, 2100):
        if date(year, month, day).weekday() == weekday:
            print year


if __name__ == '__main__':
    get_year_by_date_and_weekday(12, 24, 6)
