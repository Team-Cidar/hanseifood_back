from .abstract_service import AbstractService
from ..core.apis.kakao import KakaoApi
from ..core.utils.jwt_utils import get_token
from ..enums.role_enums import UserRole
from ..models import User
from ..responses.objs.login import UserLoginModel
from ..repositories.user_respository import UserRepository


class LoginService(AbstractService):
    def __init__(self):
        self.__user_repository = UserRepository()

    def do_login(self, code: str) -> UserLoginModel:
        # for kakao OAuth2
        kakao_access_token: str = KakaoApi.request_kakao_token(code)

        kakao_user_info: dict = KakaoApi.request_kakao_user_info(kakao_access_token)

        # check user exists
        exist, user_models = self.__user_repository.existsByKakaoId(kakao_id=kakao_user_info['kakao_id'])

        if exist:
            return self._allow_login(user_models[0])

        return UserLoginModel(
            status=False,
            kakao_id=kakao_user_info['kakao_id'],
            email=kakao_user_info['kakao_email'],
            kakao_name=kakao_user_info['kakao_nickname']
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



