import requests

from .abstract_service import AbstractService
from ..enums.role_enums import UserRole
from ..models import User
from ..core.constants.strings import env_strings as env
from ..core.utils.jwt_utils import get_token
from ..responses.objs.login import UserLoginModel
from ..repositories.user_respository import UserRepository


class LoginService(AbstractService):
    def __init__(self):
        self.__user_repository = UserRepository()

    def do_login(self, code: str) -> UserLoginModel:
        # for kakao OAuth2
        header_reusable: dict = dict()
        body: dict = dict()

        header_reusable['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
        body['grant_type'] = 'authorization_code'
        body['client_id'] = env.KAKAO_REST_API_KEY
        body['redirect_uri'] = env.KAKAO_REDIRECT_URI
        body['code'] = code

        token_response = requests.post(env.KAKAO_TOKEN_API_URL, headers=header_reusable, data=body)
        token_data: dict = token_response.json()

        header_reusable['Authorization'] = f'Bearer ${token_data["access_token"]}'

        user_info_response = requests.post(env.KAKAO_USERINFO_API_URL, headers=header_reusable)

        user_data: dict = user_info_response.json()
        user_properties: dict = user_data['properties']
        kakao_id: str = str(user_data['id'])
        kakao_nickname: str = user_properties['nickname']

        # check user exists
        exist, user_models = self.__user_repository.existsByKakaoId(kakao_id=kakao_id)

        if exist:
            return self._allow_login(user_models[0])

        return UserLoginModel(
            status=False,
            kakao_id=kakao_id,
            email='',
            kakao_name=kakao_nickname
        )

    def create_user(self, data: tuple) -> UserLoginModel:
        kakao_id, email, kakao_name, nickname = data

        user: User = self.__user_repository.save(
            email=email,
            nickname=nickname,
            kakao_name=kakao_name,
            kakao_id=kakao_id,
            role=UserRole.get_default_role())
        return self._allow_login(user)

    def _allow_login(self, user: User) -> UserLoginModel:
        user = self.__user_repository.modifyLastLoginByUser(user)
        refresh_token, access_token = get_token(user)

        return UserLoginModel.from_user_model(
            status=True,
            refresh_token=refresh_token,
            access_token=access_token,
            user_model=user.to_dto()
        )



