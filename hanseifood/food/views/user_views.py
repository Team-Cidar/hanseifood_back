from django.http import HttpResponse
from requests import HTTPError
from rest_framework.decorators import api_view

from ..core.decorators.authentication_decorator import require_auth
from ..core.decorators.deserialize_decorator import deserialize
from ..core.decorators.multi_method_decorator import multi_methods
from ..core.decorators.paging_decorator import paging
from ..dtos.general.paging_dto import PagingDto
from ..dtos.requests.kakao_login_request_dto import KakaoLoginRequestDto
from ..dtos.requests.kakao_signup_request_dto import KakaoSignupRequestDto
from ..enums.role_enums import UserRole
from ..exceptions.data_exceptions import AlreadyExistsError
from ..exceptions.request_exceptions import MissingFieldError
from ..exceptions.type_exceptions import NotDtoClassError
from ..responses.error_response import ErrorResponse
from ..responses.dto_response import DtoResponse
from ..services.user_service import UserService

user_service = UserService()

# /users/login POST
@api_view(['POST'])
@deserialize
def try_login(request, data: KakaoLoginRequestDto) -> HttpResponse:
    try:
        response = user_service.do_login(data)
        return DtoResponse.response(response)
    except MissingFieldError as e:
        return ErrorResponse.response(e, 400)
    except HTTPError as e:
        return ErrorResponse.response(e, e.response.status_code)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)

# /users POST
@deserialize
def create_user(request, data: KakaoSignupRequestDto) -> HttpResponse:
    try:
        response = user_service.create_user(data)
        return DtoResponse.response(response, 201)
    except MissingFieldError as e:
        return ErrorResponse.response(e, 400)
    except AlreadyExistsError as e:
        return ErrorResponse.response(e, 400)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)

# /users GET
@require_auth([UserRole.ADMIN, UserRole.MANAGER])
@paging()
def get_users(request, paging_data: PagingDto):
    try:
        response = user_service.get_users(paging_data)
        return DtoResponse.response(response, 200)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)

# /users GET POST
@api_view(['GET', 'POST'])
@multi_methods(GET=get_users, POST=create_user)
def users_multi_methods_acceptor():
    pass