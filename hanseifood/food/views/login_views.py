from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json

from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.type_exceptions import NotAbstractModelError
from ..responses.error_response import ErrorResponse
from ..responses.model_response import ModelResponse
from ..services.login_service import LoginService

login_service = LoginService()


@api_view(['POST'])
@csrf_exempt
def try_login(request) -> HttpResponse:
    try:
        code = json.loads(request.body).get("code")
        response = login_service.do_login(code)
        return ModelResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


@api_view(['POST'])
@csrf_exempt
def set_nickname(request) -> HttpResponse:
    try:
        custom_nickname = json.loads(request.body).get("nickname")
        kakao_nickname = json.loads(request.body).get("kakaonickname")
        user_id = json.loads(request.body).get("id")
        data = {"nickname": custom_nickname,
                "kakaonickname": kakao_nickname,
                "id": user_id}
        response = login_service.set_user_nickname(data)
        return ModelResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)
