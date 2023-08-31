from datetime import datetime

from django.http import HttpResponse

from .objs.menu import MenuModel
from .responses.model_response import ModelResponse
from .utils.menus import get_daily_menu
from .utils.dates import get_dates_in_this_week


def index(request):
    return HttpResponse("Hello world!")


# /menus/day GET
def get_todays_menu(request):
    today = datetime.today()

    response = MenuModel()

    response = get_daily_menu(today, response)

    if len(response.student_menu) == 0:
        response.only_employee = True

    return ModelResponse.getResponse(response)


# /menus/week GET
def get_weekly_menus(request):
    this_week = get_dates_in_this_week()

    response = MenuModel()
    for day in this_week:
        response = get_daily_menu(day, response)

    if len(response.student_menu) == 0:
        response.only_employee = True

    return ModelResponse.getResponse(response)