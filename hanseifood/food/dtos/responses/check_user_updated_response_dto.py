from .user_login_response_dto import UserLoginResponseDto
from ..abstract_dto import Dto


class CheckUserUpdatedResponseDto(Dto):
    def __init__(self, user: UserLoginResponseDto=None):
        self.updated: bool = True if user else False
        if self.updated:
            self.user: UserLoginResponseDto = user
