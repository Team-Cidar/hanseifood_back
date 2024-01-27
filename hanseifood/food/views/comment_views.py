from django.core.paginator import EmptyPage
from django.http import HttpResponse
from rest_framework.decorators import api_view

from ..core.decorators.deserialize_decorator import deserialize
from ..core.decorators.authentication_decorator import require_auth
from ..core.decorators.multi_method_decorator import multi_methods
from ..core.decorators.paging_decorator import paging
from ..dtos.general.paging_dto import PagingDto
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


# /comments/menus POST
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


# /comments/menus DELETE
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


# /comments/menus GET
@deserialize
@paging()
def get_comment_by_menu_id(request, data: GetCommentRequestDto, paging_data: PagingDto) -> HttpResponse:
    try:
        response = comment_service.get_comment_by_menu_id(data=data, paging_data=paging_data)
        return DtoResponse.response(response, 200)
    except EmptyPage as e:
        return ErrorResponse.response(e, 400)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /comments/menus/users GET
@api_view(['GET'])
@require_auth()
@paging()
def get_comment_by_user(request, user: User, paging_data: PagingDto) -> HttpResponse:
    try:
        response = comment_service.get_comment_by_user(user=user, paging_data=paging_data)
        return DtoResponse.response(response, 200)
    except EmptyPage as e:
        return ErrorResponse.response(e, 400)
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


# /comments GET POST DELETE
@api_view(['GET', 'POST', 'DELETE'])
@multi_methods(GET=get_comment_by_menu_id, POST=add_comment, DELETE=delete_comment)
def comments_multi_methods_acceptor():
    pass


# /comments/report POST GET
@api_view(['POST', 'GET'])
@multi_methods(POST=report_comment, GET=get_reported_comment)
def comments_report_methods_acceptor():
    pass