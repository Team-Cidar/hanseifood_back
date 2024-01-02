import requests
from datetime import datetime
from django.db.models import QuerySet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .abstract_service import AbstractService
from ..core.jwt.serializers import MyTokenObtainPairSerializer
from ..models import User
from ..core.constants.strings.login_string import TOKEN_NOT_EXISTS, NICKNAME_NOT_EXISTS
from ..core.constants.strings import env_strings as env
from ..responses.objs.login import UserModel, UserLoginModel
from ..repositories.user_respository import UserRepository


class LoginService(AbstractService):
    def __init__(self):
        # Todo: add repository classes here and use
        self.__user_repository = UserRepository()
        pass

    def do_login(self, code: str) -> UserLoginModel:
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

        kakao_response = requests.post("https://kapi.kakao.com/v2/user/me", headers=header)

        user_data: dict = kakao_response.json()
        user_properties: dict = user_data['properties']
        kakao_id: str = str(user_data['id'])
        kakao_nickname: str = user_properties['nickname']

        user_models: QuerySet = User.objects.filter(kakao_id=kakao_id)
        response: UserLoginModel
        if user_models.exists():
            # send token, return user response with success is true
            # token must have user id, is admin field
            user: User = user_models[0]
            user.last_login = datetime.today()
            user.save()
            token = MyTokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            # token
            return UserLoginModel.from_user_model(
                status=True,
                refresh_token=refresh_token,
                access_token=access_token,
                user_model=user.to_dto()
            )

        response = UserLoginModel(
            status=False,
            kakao_id=kakao_id,
            password='',
            email='',
            kakao_name=kakao_nickname,
            is_admin=False,
            nickname=''
        )
        # client must get user nickname from user, and send user response with the user selected nickname to create user.
        return response

    def create_user(self, data: tuple) -> UserModel:
        kakao_id, email, kakao_name, nickname = data

        user: User = User.objects.create_user(email=email, nickname=nickname, kakao_name=kakao_name, kakao_id=kakao_id)
        user.last_login = datetime.today()
        user.save()

        token = MyTokenObtainPairSerializer.get_token(user)
        # 이렇게 하면 토큰 생성되는 듯 하고
        # JWTAuthentication.authenticate(request) 하면 토큰 뽑아와서 인증처리 해서 토큰 데이터 뽑아주는 듯함
        # 토큰 유효성 검사 쪽은 Serializer 상속받아서 그 메서드에서 구현해서 가져다가 쓰거나 다른 방법 있는지 확인하면 될것 같고
        # 다 끝내고 코드 리팩터링 하자

        refresh_token = str(token)
        access_token = str(token.access_token)
        user_dto: UserModel = user.to_dto()

        return UserLoginModel.from_user_model(
            status=True,
            refresh_token=refresh_token,
            access_token=access_token,
            user_model=user_dto
        )



