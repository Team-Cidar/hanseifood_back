from datetime import datetime

from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view

from ..core.decorators.deserialize_decorator import deserialize
from ..core.decorators.authentication_decorator import require_auth
from ..dtos.model_mapped.user_dto import UserDto
from ..dtos.requests.add_comment_request_dto import AddCommentRequestDto
from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.type_exceptions import NotDtoClassError
from ..models import User
from ..responses.error_response import ErrorResponse
from ..responses.dto_response import DtoResponse
from ..services.comment_service import CommentService

comment_service = CommentService()


# /comment POST
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