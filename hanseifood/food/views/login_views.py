from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from ..core.utils.request_utils import extract_request_datas
from ..exceptions.request_exceptions import MissingFieldError
from ..exceptions.type_exceptions import NotAbstractModelError
from ..responses.error_response import ErrorResponse
from ..responses.model_response import ModelResponse
from ..services.login_service import LoginService

login_service = LoginService()


@api_view(['POST'])
@csrf_exempt
def try_login(request) -> HttpResponse:
    try:
        code = extract_request_datas(request.data, ['code'])
        response = login_service.do_login(code)
        return ModelResponse.response(response)
    except MissingFieldError as e:
        return ErrorResponse.response(e, 400)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


@api_view(['POST'])
@csrf_exempt
def create_user(request) -> HttpResponse:
    try:
        # handle user already exists error
        data = extract_request_datas(request.data, ['kakao_id', 'email', 'kakao_name', 'nickname'])
        response = login_service.create_user(data)
        return ModelResponse.response(response, status_code=201)
    except MissingFieldError as e:
        return ErrorResponse.response(e, 400)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)
