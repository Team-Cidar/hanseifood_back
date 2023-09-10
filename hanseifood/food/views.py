from django.http import HttpResponse, HttpRequest

from .responses.model_response import ModelResponse
from .services.menu_service import MenuService

import datetime

menu_service = MenuService()


def index(request):
    return HttpResponse("Hello world!")


# /menus/day GET
def get_todays_menu(request):
    response = menu_service.get_one_day_menu()

    return ModelResponse.getResponse(response)


# /menus/week GET
def get_weekly_menus(request):
    response = menu_service.get_this_week_menu()

    return ModelResponse.getResponse(response)


# /menus/target? GET
def get_target_days_menu(request: HttpRequest):
    date = request.GET.get('date', None)
    date = datetime.datetime.strptime(date, '%Y%m%d')
    response = menu_service.get_target_days_menu(date)
    return ModelResponse.getResponse(response)

