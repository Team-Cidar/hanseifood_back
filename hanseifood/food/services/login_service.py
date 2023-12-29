import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
from ..core.constants.strings.login_string import TOKEN_NOT_EXISTS, NICKNAME_NOT_EXISTS
from ..repositories.login_repository import LoginRepository
from ..responses.objs.login import UserModel


class LoginService:
    def __init__(self):
        self.__login_repository = LoginRepository()

    @method_decorator(csrf_exempt, name='dispatch')
    def do_login(self, request) -> UserModel:

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

        existing_user = self.__login_repository.findByID(id)
        existing_user2 = self.__login_repository.findByID2(id)

        if existing_user is None:
            self.__login_repository.createUser(id, nickname)
            return UserModel(user_id=id, user_nickname=nickname, is_exists=False, customnickname=NICKNAME_NOT_EXISTS,
                             access_token=TOKEN_NOT_EXISTS)
        elif existing_user2:
            return UserModel(user_id=id, user_nickname=nickname, is_exists=False, customnickname=NICKNAME_NOT_EXISTS,
                             access_token=TOKEN_NOT_EXISTS)
        else:
            body = {
                "username": id,
                "password": nickname,
            }

            token_response = requests.post('http://localhost:8000/api/token', data=body)

            token_data = token_response.json()
            access_token = token_data.get("access")

            return UserModel(user_id=id, user_nickname=nickname, is_exists=True, customnickname=existing_user.nickname,
                             access_token=access_token)

    @method_decorator(csrf_exempt, name='dispatch')
    def set_user_nickname(self, request) -> UserModel:

        self.__login_repository.saveNickName(request['id'], request['nickname'])

        body = {
            "username": request['id'],
            "password": request['kakaonickname'],
        }
        print(body)
        token_response = requests.post('http://localhost:8000/api/token', data=body)

        token_data = token_response.json()
        access_token = token_data.get("access")
        print(access_token)

        return UserModel(user_id=request['id'], user_nickname=request['kakaonickname'], is_exists=True,
                         customnickname=request['nickname'], access_token=access_token)
