import os

from ..models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
import json
import requests

from ..responses.objs.login import LoginModel

id = None
nickname = None
token = None

class LoginService:

    @method_decorator(csrf_exempt, name='dispatch')
    def do_login(self, request) -> LoginModel:
        global token
        global id
        global nickname

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        body = {
            'grant_type': 'authorization_code',
            'client_id': os.getenv("KAKAO_REST_API_KEY"),
            'redirect_uri': 'http://localhost:8080/login/confirm',
            'code': request,
        }

        response = requests.post(os.getenv("kakao_token_api"), headers=headers, data=body)

        data = response.json()
        token = data.get('access_token')

        headers = {
            'Authorization': f'Bearer ${token}'
        }
        response = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers)

        data = response.json()
        id = data.get('id')
        data2 = data.get('properties')
        nickname = data2.get('nickname')
        print(nickname)

        existing_user = CustomUser.objects.filter(username=id).first()
        existing_user2 = CustomUser.objects.filter(username=id, nickname="").first()

        print(existing_user)

        if existing_user is None :
            user, created = CustomUser.objects.get_or_create(username=id, kakaonickname=nickname)
            user.set_password(nickname)
            user.save()
            return LoginModel(user_id=id, user_nickname=nickname, is_exists=False,customnickname="생성전" , access_token="없음")
        elif existing_user2:
            return LoginModel(user_id=id, user_nickname=nickname, is_exists=False, customnickname="생성전" , access_token="없음")
        else:
            body = {
                "username": id,
                "password": nickname,
            }

            token_response = requests.post('http://localhost:8000/api/token', data=body)

            token_data = token_response.json()
            access_token = token_data.get("access")
            print(access_token)
            return LoginModel(user_id=id, user_nickname=nickname, is_exists=True, customnickname=existing_user.nickname, access_token=access_token)

    @method_decorator(csrf_exempt, name='dispatch')
    def set_user_nickname(self, request) -> LoginModel:

        print(id)
        print(request)

        new_user = CustomUser.objects.filter(username=id).first()

        new_user.nickname = request
        new_user.save()

        body = {
        "username": id,
        "password": nickname,
        }

        token_response = requests.post('http://localhost:8000/api/token', data=body)

        token_data = token_response.json()
        access_token = token_data.get("access")
        print(access_token)

        return LoginModel(user_id = id, user_nickname=nickname, is_exists=True, customnickname=request, access_token=access_token)


