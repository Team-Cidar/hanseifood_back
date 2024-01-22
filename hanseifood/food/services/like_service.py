import logging

from .abstract_service import AbstractService
from ..dtos.requests.like_request_dto import LikeRequestDto
from ..dtos.responses.count_like_response_dto import CountLikeResponseDto
from ..dtos.responses.toggle_like_response_dto import ToggleLikeResponseDto
from ..models import User
from ..repositories.menu_like_repository import MenuLikeRepository

logger = logging.getLogger(__name__)


class LikeService(AbstractService):
    def __init__(self):
        self.__menu_like_repository = MenuLikeRepository()

    def toggle_like(self, data: LikeRequestDto, user: User):
        exists, like = self.__menu_like_repository.existByMenuIdAndUserId(menu_id=data.menu_id, user_id=user)
        if exists:
            self.__menu_like_repository.delete(like[0])
            like_count: int = self.__menu_like_repository.countByMenuId(data.menu_id)
            return ToggleLikeResponseDto(menu_id=data.menu_id, like_count=like_count, like=False)

        self.__menu_like_repository.save(menu_id=data.menu_id, user_id=user)
        like_count: int = self.__menu_like_repository.countByMenuId(data.menu_id)
        return ToggleLikeResponseDto(menu_id=data.menu_id, like_count=like_count, like=True)

    def count_like_by_menu_id(self, data: LikeRequestDto):
        like_count: int = self.__menu_like_repository.countByMenuId(menu_id=data.menu_id)
        return CountLikeResponseDto(menu_id=data.menu_id, like_count=like_count)


