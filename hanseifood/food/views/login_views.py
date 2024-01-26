from django.http import HttpResponse
from requests import HTTPError
from rest_framework.decorators import api_view

from ..core.decorators.deserialize_decorator import deserialize
from ..dtos.requests.kakao_login_request_dto import KakaoLoginRequestDto
from ..dtos.requests.kakao_signup_request_dto import KakaoSignupRequestDto
from ..exceptions.data_exceptions import AlreadyExistsError
from ..exceptions.request_exceptions import MissingFieldError
from ..exceptions.type_exceptions import NotDtoClassError
from ..responses.error_response import ErrorResponse
from ..responses.dto_response import DtoResponse
from ..services.login_service import LoginService

login_service = LoginService()

# /login POST
@api_view(['POST'])
@deserialize
def try_login(request, data: KakaoLoginRequestDto) -> HttpResponse:
    try:
        response = login_service.do_login(data)
        return DtoResponse.response(response)
    except MissingFieldError as e:
        return ErrorResponse.response(e, 400)
    except HTTPError as e:
        return ErrorResponse.response(e, e.response.status_code)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)

# /signup POST
@api_view(['POST'])
@deserialize
def create_user(request, data: KakaoSignupRequestDto) -> HttpResponse:
    try:
        response = login_service.create_user(data)
        return DtoResponse.response(response, 201)
    except MissingFieldError as e:
        return ErrorResponse.response(e, 400)
    except AlreadyExistsError as e:
        return ErrorResponse.response(e, 400)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)
