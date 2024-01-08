from ..abstract_dto import Dto
from ..model_mapped.user_dto import UserDto


class UserLoginResponseDto(Dto):
    def __init__(self, user: UserDto):
        self.status: bool = False
        self.refresh_token: str = ''
        self.access_token: str = ''
        self.user: UserDto = user
