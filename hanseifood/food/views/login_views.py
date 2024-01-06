from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from requests import HTTPError
from rest_framework.decorators import api_view

from ..core.decorators.deserialize_decorator import deserialize
from ..dtos.requests.kakao_login_request_dto import KakaoLoginRequestDto
from ..dtos.requests.kakao_signup_request_dto import KakaoSignupRequestDto
from ..exceptions.data_exceptions import AlreadyExistsError
from ..exceptions.request_exceptions import MissingFieldError
from ..exceptions.type_exceptions import NotAbstractModelError
from ..responses.error_response import ErrorResponse
from ..responses.model_response import ModelResponse
from ..services.login_service import LoginService

login_service = LoginService()

# /login POST
@api_view(['POST'])
@csrf_exempt
@deserialize
def try_login(request, data: KakaoLoginRequestDto) -> HttpResponse:
    try:
        response = login_service.do_login(data)
        return ModelResponse.response(response)
    except MissingFieldError as e:
        return ErrorResponse.response(e, 400)
    except HTTPError as e:
        return ErrorResponse.response(e, e.response.status_code)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)

# /signup POST
@api_view(['POST'])
@csrf_exempt
@deserialize
def create_user(request, data: KakaoSignupRequestDto) -> HttpResponse:
    try:
        response = login_service.create_user(data)
        return ModelResponse.response(response, 201)
    except MissingFieldError as e:
        return ErrorResponse.response(e, 400)
    except AlreadyExistsError as e:
        return ErrorResponse.response(e, 400)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)
