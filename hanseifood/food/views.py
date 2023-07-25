from datetime import datetime, timedelta

from django.http import HttpResponse, JsonResponse
from .models import Day, Meal, DayMeal
from .response_objs.menuResponse import MenuResponse
from .utils.menus import getDailyMenu
from .utils.dates import getDatesInThisWeek


def index(request):
    return HttpResponse("Hello world!")


# /menus/day GET
def get_todays_menu(request):
    today = datetime.today()

    response = getDailyMenu(today)
    response_json = response.toJson()

    return HttpResponse(response_json)


# /menus/week
def get_weekly_menus(request):
    this_week = getDatesInThisWeek()

    responses = []
    for day in this_week:
        daily_menu = getDailyMenu(day)
        responses.append(daily_menu)

    return HttpResponse(MenuResponse.listToJson(responses))
