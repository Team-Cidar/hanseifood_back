from ..abstract_dto import Dto
from ...enums.role_enums import UserRole
from ...models import User


class UserDto(Dto):
    def __init__(self):
        self.kakao_id: str = ''
        self.email: str = ''
        self.kakao_name: str = ''
        self.nickname: str = ''
        self.is_admin: bool = False
        self.role: UserRole = UserRole.get_default_role()

    @classmethod
    def from_model(cls, user_model: User):
        user: UserDto = cls()
        user.kakao_id = user_model.kakao_id
        user.email = user_model.email
        user.kakao_name = user_model.kakao_name
        user.nickname = user_model.nickname
        user.is_admin = user_model.is_admin
        user.role = UserRole.from_value(user_model.role)
        return user

    @classmethod
    def get_dummy_kakao_user(cls, kakao_info: dict):
        user: UserDto = cls()
        user.kakao_id = kakao_info['kakao_id']
        user.email = kakao_info['kakao_email']
        user.kakao_name = kakao_info['kakao_nickname']
        return user

