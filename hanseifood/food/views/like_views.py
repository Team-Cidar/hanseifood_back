from django.http import HttpResponse
from rest_framework.decorators import api_view

from ..core.decorators.deserialize_decorator import deserialize
from ..core.decorators.authentication_decorator import require_auth
from ..core.decorators.multi_method_decorator import multi_methods
from ..core.decorators.paging_decorator import paging
from ..dtos.general.paging_dto import PagingDto
from ..dtos.requests.like_request_dto import LikeRequestDto
from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.type_exceptions import NotDtoClassError
from ..models import User
from ..responses.error_response import ErrorResponse
from ..responses.dto_response import DtoResponse
from ..services.like_service import LikeService

like_service = LikeService()


# /likes/menus POST
@require_auth()
@deserialize
def toggle_like(request, data: LikeRequestDto, user: User) -> HttpResponse:
    try:
        response = like_service.toggle_like(data=data, user=user)
        if response.like:
            return DtoResponse.response(response, 201)
        else:
            return DtoResponse.response(response, 200)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /likes/menus GET
@deserialize
def count_likes_by_menu_id(request, data: LikeRequestDto) -> HttpResponse:
    try:
        response = like_service.count_like_by_menu_id(data=data)
        return DtoResponse.response(response, 200)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /likes/menus/user GET
@api_view(['GET'])
@require_auth()
@paging()
def get_liked_menus_by_user(request, user: User, paging_data: PagingDto) -> HttpResponse:
    try:
        response = like_service.get_liked_menus_by_user(user=user, paging_data=paging_data)
        return DtoResponse.response(response, 200)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


@api_view(['GET', 'POST'])
@multi_methods(GET=count_likes_by_menu_id, POST=toggle_like)
def like_multi_methods_acceptor():
    pass