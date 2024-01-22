from django.http import HttpResponse
from rest_framework.decorators import api_view

from ..core.decorators.deserialize_decorator import deserialize
from ..core.decorators.authentication_decorator import require_auth
from ..dtos.requests.add_comment_request_dto import AddCommentRequestDto
from ..dtos.requests.get_comment_request_dto import GetCommentRequestDto
from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.type_exceptions import NotDtoClassError
from ..models import User
from ..responses.error_response import ErrorResponse
from ..responses.dto_response import DtoResponse
from ..services.comment_service import CommentService

comment_service = CommentService()


# /comments POST
@api_view(['POST'])
@require_auth()
@deserialize
def add_comment(request, data: AddCommentRequestDto, user: User) -> HttpResponse:
    try:
        response = comment_service.add_comment(data=data, user=user)
        return DtoResponse.response(response, 201)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /comments
@api_view(['GET'])
@deserialize
def get_comment_by_menu_id(request, data: GetCommentRequestDto) -> HttpResponse:
    try:
        response = comment_service.get_comment_by_menu_id(data=data)
        return DtoResponse.response(response, 200)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


@api_view(['GET'])
@require_auth()
def get_comment_by_user(request, user: User) -> HttpResponse:
    try:
        response = comment_service.get_comment_by_user(user=user)
        return DtoResponse.response(response, 200)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)