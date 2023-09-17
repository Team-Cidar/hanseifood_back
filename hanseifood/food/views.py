from django.http import HttpResponse, HttpRequest

from .exceptions.menu_exceptions import EmptyDataError
from .exceptions.type_exceptions import NotAbstractModelError
from .responses.error_response import ErrorResponse
from .responses.model_response import ModelResponse
from .services.menu_service import MenuService

import datetime

menu_service = MenuService()


def index(request):
    return HttpResponse("Hello world!")


# /menus/day GET
def get_todays_menu(request):
    try:
        response = menu_service.get_one_day_menu()
        return ModelResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /menus/week GET
def get_weekly_menus(request):
    try:
        response = menu_service.get_this_week_menu()
        return ModelResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /menus/target? GET
def get_target_days_menu(request: HttpRequest):
    try:
        date = request.GET.get('date', None)
        date = datetime.datetime.strptime(date, '%Y%m%d')
        response = menu_service.get_target_days_menu(date)
        return ModelResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)
