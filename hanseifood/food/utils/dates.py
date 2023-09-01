from datetime import datetime, timedelta, date
import math


def get_dates_in_this_week(start=0, end=4, today=date.today()):
    """returns all dates of the week. If you don't set start and end parameter, it'll return a list from monday to friday.

    Parameters
    ----------
    start : int
        start day of the week.
        range(0~6)
    end : int
        end day of the week.
        range(0~6)
    today : date
        date included in the week you want to get.

    Returns
    -------
    list
        dates in the week

    See Also
    --------
    'day' used in 'start' and 'end' arguments is an integer type number that indicates the day of the week.
    For example, 0 means Monday, 1 means Tuesday, ~~ 6 means Sunday.

    """
    day = today.weekday()
    monday = today
    if day != 0:
        monday = today + timedelta(days=(start - day))

    dates = []
    for day in range(end - start + 1):
        dates.append(monday + timedelta(days=day))

    return dates


def get_week_number(today=datetime.today()):
    first_day = today.replace(day=1)
    first_sunday = first_day + timedelta(days=6 - first_day.weekday())
    days_after_fir_sunday = (today - first_sunday).days
    if days_after_fir_sunday <= 0:  # bef first sunday
        week_of_month = 1
    else:
        week_of_month = math.ceil(days_after_fir_sunday / 7) + 1

    if first_day.weekday() in [5, 6]:  # if month starts in sat or sun
        week_of_month -= 1

    return week_of_month


def get_weekday(today_date):
    day = today_date.weekday()
    if day in [5, 6]:  # [sat, sun]
        today_date -= timedelta(days=day - 4)  # get friday
    return today_date
