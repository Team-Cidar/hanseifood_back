from typing import List

from django.core.paginator import Page
from django.db.models import QuerySet

from .abstract_service import AbstractService
from ..core.apis.kakao import KakaoApi
from ..core.utils import jwt_utils as jwt
from ..dtos.general.paging_dto import PagingDto, PagingResponseDto
from ..dtos.model_mapped.user_dto import UserDto
from ..dtos.requests.kakao_login_request_dto import KakaoLoginRequestDto
from ..dtos.requests.kakao_signup_request_dto import KakaoSignupRequestDto
from ..dtos.responses.check_user_updated_response_dto import CheckUserUpdatedResponseDto
from ..dtos.responses.user_login_response_dto import UserLoginResponseDto
from ..enums.role_enums import UserRole
from ..exceptions.data_exceptions import AlreadyExistsError
from ..models import User
from ..repositories.user_respository import UserRepository


class UserService(AbstractService):
    def __init__(self):
        self.__user_repository = UserRepository()

    def do_login(self, data: KakaoLoginRequestDto) -> UserLoginResponseDto:
        # for kakao OAuth2
        kakao_access_token: str = KakaoApi.request_kakao_token(data.code)

        kakao_user_info: dict = KakaoApi.request_kakao_user_info(kakao_access_token)

        # check user exists
        exist, user_models = self.__user_repository.existsByKakaoId(kakao_id=kakao_user_info['kakao_id'])

        if exist:
            return self.__allow_login(user_models[0])

        return UserLoginResponseDto(
            user=UserDto.get_dummy_kakao_user(
                kakao_info=kakao_user_info
            )
        )

    def create_user(self, data: KakaoSignupRequestDto) -> UserLoginResponseDto:
        exists, _ = self.__user_repository.existsByKakaoId(kakao_id=data.kakao_id)
        if exists:
            raise AlreadyExistsError(data.kakao_id)

        user: User = self.__user_repository.save(
            email=data.email,
            nickname=data.nickname,
            kakao_name=data.kakao_name,
            kakao_id=data.kakao_id,
            role=UserRole.get_default_role())
        return self.__allow_login(user)

    def get_users(self, paging_data: PagingDto) -> PagingResponseDto:
        response: List[UserDto]
        users: QuerySet = self.__user_repository.all()
        sorted_users: QuerySet = users.order_by('created_at')
        page: Page = self.__user_repository.get_page(sorted_users, paging_data)

        response = [UserDto.from_model(user) for user in page.object_list]
        return PagingResponseDto(page, response)

    def check_modified(self, user: User) -> CheckUserUpdatedResponseDto:
        user: User = self.__user_repository.findByKakaoId(user.kakao_id)[0]
        if user.last_login < user.updated_at:
            return CheckUserUpdatedResponseDto(self.__allow_login(user))
        return CheckUserUpdatedResponseDto()


    def __allow_login(self, user: User) -> UserLoginResponseDto:
        user = self.__user_repository.modifyLastLoginByUser(user)
        refresh_token, access_token = jwt.get_token(user)

        response: UserLoginResponseDto = UserLoginResponseDto(user=UserDto.from_model(user))
        response.status = True
        response.refresh_token = refresh_token
        response.access_token = access_token

        return response



