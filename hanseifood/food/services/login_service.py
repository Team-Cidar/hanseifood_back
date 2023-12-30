import os
import requests

from ..models import CustomUser
from ..core.constants.strings.login_string import TOKEN_NOT_EXISTS, NICKNAME_NOT_EXISTS
from ..core.constants.strings import env_strings as env
from ..responses.objs.login import UserModel
from .abstract_service import AbstractService


class LoginService(AbstractService):
    def __init__(self):
        # Todo: add repository classes here and use
        pass

    def do_login(self, request) -> UserModel:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        body = {
            'grant_type': 'authorization_code',
            'client_id': env.KAKAO_REST_API_KEY,
            'redirect_uri': 'http://localhost:8080/login/confirm',
            'code': request,
        }

        response = requests.post(env.KAKAO_TOKEN_API_URL, headers=headers, data=body)

        data = response.json()
        token = data.get('access_token')

        headers = {
            'Authorization': f'Bearer ${token}'
        }
        response = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers)

        data = response.json()
        user_id = data.get('id')
        data2 = data.get('properties')
        nickname = data2.get('nickname')

        existing_user = CustomUser.objects.filter(username=user_id).first()
        existing_user2 = CustomUser.objects.filter(username=user_id, nickname="").first()

        if existing_user is None :
            user, created = CustomUser.objects.get_or_create(username=user_id, kakaonickname=nickname)
            user.set_password(nickname)
            user.save()
            return UserModel(user_id=user_id, user_nickname=nickname, is_exists=False,customnickname=NICKNAME_NOT_EXISTS , access_token=TOKEN_NOT_EXISTS)
        elif existing_user2:
            return UserModel(user_id=user_id, user_nickname=nickname, is_exists=False, customnickname=NICKNAME_NOT_EXISTS , access_token=TOKEN_NOT_EXISTS)
        else:
            body = {
                "username": user_id,
                "password": nickname,
            }

            token_response = requests.post('http://localhost:8000/api/token', data=body)

            token_data = token_response.json()
            access_token = token_data.get("access")
            return UserModel(user_id=user_id, user_nickname=nickname, is_exists=True, customnickname=existing_user.nickname, access_token=access_token)

    def set_user_nickname(self, request) -> UserModel:
        new_user = CustomUser.objects.filter(username=request['id']).first()

        new_user.nickname = request['nickname']
        new_user.save()

        body = {
        "username": request['id'],
        "password": request['kakaonickname'],
        }
        token_response = requests.post('http://localhost:8000/api/token', data=body)

        token_data = token_response.json()
        access_token = token_data.get("access")

        return UserModel(user_id=request['id'], user_nickname=request['kakaonickname'], is_exists=True, customnickname=request['nickname'], access_token=access_token)
