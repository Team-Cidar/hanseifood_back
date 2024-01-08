from ..abstract_dto import Dto
from ..common.user_dto import UserDto


class UserLoginResponseDto(Dto):
    def __init__(self, user: UserDto):
        self.status: bool = False
        self.refresh_token: str = ''
        self.access_token: str = ''
        self.user: UserDto = user
