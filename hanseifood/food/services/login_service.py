import requests
from django.db.models import QuerySet

from .abstract_service import AbstractService
from ..models import User
from ..core.constants.strings.login_string import TOKEN_NOT_EXISTS, NICKNAME_NOT_EXISTS
from ..core.constants.strings import env_strings as env
from ..responses.objs.login import UserModel
from ..repositories.user_respository import UserRepository


class LoginService(AbstractService):
    def __init__(self):
        # Todo: add repository classes here and use
        self.__user_repository = UserRepository()
        pass

    def do_login(self, code: str) -> UserModel:
        header: dict = dict()
        body: dict = dict()

        header['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
        body['grant_type'] = 'authorization_code'
        body['client_id'] = env.KAKAO_REST_API_KEY
        body['redirect_uri'] = env.KAKAO_REDIRECT_URI
        body['code'] = code

        token_response = requests.post(env.KAKAO_TOKEN_API_URL, headers=header, data=body)
        token_data: dict = token_response.json()

        header['Authorization'] = f'Bearer ${token_data["access_token"]}'

        response = requests.post("https://kapi.kakao.com/v2/user/me", headers=header)

        user_data: dict = response.json()
        user_properties: dict = user_data['properties']
        user_id: str = user_data['id']
        nickname: str = user_properties['nickname']

        exist, user_model = self.__user_repository.existsByUsername(username=user_id)

        if exist:
            # 존재하면 토큰발행, response로 유저객체 넘겨주기, success true
            pass

        # 없으면 카카오 OAuth2 정보 넘겨주기, success false

        existing_user = CustomUser.objects.filter(username=user_id).first()
        existing_user2 = CustomUser.objects.filter(username=user_id, nickname="").first()

        if existing_user is None:
            user: CustomUser
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
