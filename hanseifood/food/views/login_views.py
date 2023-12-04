from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import json
from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.type_exceptions import NotAbstractModelError
from ..responses.error_response import ErrorResponse
from ..responses.model_response import ModelResponse
from ..services.login_service import LoginService

login_service = LoginService()

@method_decorator(csrf_exempt, name='dispatch')
def try_login(request) -> HttpResponse:
    try:
        code = json.loads(request.body).get("code")
        print(code)
        response = login_service.do_login(code)
        return ModelResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)

@method_decorator(csrf_exempt, name='dispatch')
def set_nickname(request) -> HttpResponse:
    try:
        custom_nickname = json.loads(request.body).get("nickname")
        print(custom_nickname)
        response = login_service.set_user_nickname(custom_nickname)
        return ModelResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)
            token['is_staff'] = user.is_staff  # 확장
            token['is_superuser'] = user.is_superuser  # 확장
            token['nickname'] = user.nickname
            return token

class MyTokenObtainPairView(TokenObtainPairView):
        serializer_class = MyTokenObtainPairSerializer