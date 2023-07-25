from datetime import datetime, timedelta


def getDatesInThisWeek(start=0, end=4, today=datetime.today()):
    """returns all dates of the week. If you don't set start and end parameter, it'll return a list from monday to friday.

    Parameters
    ----------
    start: int
        start day of the week.
        range(0~6)
    end : int
        end day of the week.
        range(0~6)
    today : datetime
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


