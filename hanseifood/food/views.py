from datetime import datetime

from django.http import HttpResponse
from .responses.menu import MenuResponse
from .utils.menus import get_daily_menu
from .utils.dates import get_dates_in_this_week


def index(request):
    return HttpResponse("Hello world!")


# /menus/day GET
def get_todays_menu(request):
    today = datetime.today()

    response = get_daily_menu(today)
    response_json = response.toJson()

    return HttpResponse(response_json)


# /menus/week GET
def get_weekly_menus(request):
    this_week = get_dates_in_this_week()

    responses = []
    for day in this_week:
        daily_menu = get_daily_menu(day)
        responses.append(daily_menu)

    return HttpResponse(MenuResponse.listToJson(responses))
