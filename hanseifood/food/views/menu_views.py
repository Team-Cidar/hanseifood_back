from datetime import datetime

from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view

from ..core.decorators.deserialize_decorator import deserialize
from ..dtos.requests.get_target_menu_request_dto import GetTargetMenuRequestDto
from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.type_exceptions import NotDtoClassError
from ..responses.error_response import ErrorResponse
from ..responses.dto_response import DtoResponse
from ..services.menu_service import MenuService

menu_service = MenuService()


# /menus/day GET
@api_view(['GET'])
def get_today_menu(request) -> HttpResponse:
    try:
        response = menu_service.get_today_menu()
        return DtoResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /menus/week GET
@api_view(['GET'])
def get_weekly_menus(request) -> HttpResponse:
    try:
        response = menu_service.get_weekly_menu()
        return DtoResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /menus/target? GET
@api_view(['GET'])
@deserialize
def get_target_days_menu(request: HttpRequest, data: GetTargetMenuRequestDto) -> HttpResponse:
    try:
        date = datetime.strptime(data.date, '%Y%m%d')
        response = menu_service.get_target_days_menu(date)
        return DtoResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


@api_view(['GET'])
def get_menus_by_id(request, menu_id: str) -> HttpResponse:
    try:
        response = menu_service.get_by_menu_id(menu_id)
        return DtoResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)
