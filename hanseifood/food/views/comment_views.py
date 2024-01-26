from django.http import HttpResponse
from rest_framework.decorators import api_view

from ..core.decorators.deserialize_decorator import deserialize
from ..core.decorators.authentication_decorator import require_auth
from ..core.decorators.multi_method_decorator import multi_methods
from ..dtos.requests.add_comment_request_dto import AddCommentRequestDto
from ..dtos.requests.delete_comment_request_dto import DeleteCommentRequestDto
from ..dtos.requests.get_comment_request_dto import GetCommentRequestDto
from ..dtos.requests.report_comment_request_dto import ReportCommentRequestDto
from ..enums.role_enums import UserRole
from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.jwt_exceptions import PermissionDeniedError
from ..exceptions.request_exceptions import EmptyValueError
from ..exceptions.type_exceptions import NotDtoClassError
from ..models import User
from ..responses.error_response import ErrorResponse
from ..responses.dto_response import DtoResponse
from ..services.comment_service import CommentService

comment_service = CommentService()


# /comments POST
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


# /comments DELETE
@require_auth()
@deserialize
def delete_comment(request, data: DeleteCommentRequestDto, user: User) -> HttpResponse:
    try:
        response = comment_service.delete_comment(data=data, user=user)
        return DtoResponse.response(response, 200)
    except PermissionDeniedError as e:
        return ErrorResponse.response(e, 403)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /comments/menu
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


# /comments/user
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


# /comments/report POST
@require_auth()
@deserialize
def report_comment(request, data: ReportCommentRequestDto, user: User) -> HttpResponse:
    try:
        response = comment_service.report_comment(data=data, user=user)
        return DtoResponse.response(response, 201)
    except EmptyValueError as e:
        return ErrorResponse.response(e, 400)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /comments/report GET
@require_auth([UserRole.ADMIN])
def get_reported_comment(request) -> HttpResponse:
    try:
        response = comment_service.get_reported_comments()
        return DtoResponse.response(response, 200)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /comments POST DELETE
@api_view(['POST', 'DELETE'])
@multi_methods(POST=add_comment, DELETE=delete_comment)
def comments_multi_methods_acceptor():
    pass


# /comments/report POST GET
@api_view(['POST', 'GET'])
@multi_methods(POST=report_comment, GET=get_reported_comment)
def comments_report_methods_acceptor():
    pass