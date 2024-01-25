from datetime import datetime

from .user_dto import UserDto
from ..abstract_dto import Dto
from ...models import MenuComment


class MenuCommentDto(Dto):
    def __init__(self, comment_id: str, menu_id: str, user_dto: UserDto, comment: str, commented_at: datetime):
        self.comment_id: str = comment_id
        self.menu_id: str = menu_id
        self.user: UserDto = user_dto
        self.comment: str = comment
        self.commented_at: datetime = commented_at

    @classmethod
    def from_model(cls, menu_comment_model: MenuComment):
        menu_comment: MenuCommentDto = cls(
            user_dto=UserDto.from_model(menu_comment_model.user_id),
            comment_id=str(menu_comment_model.comment_id),
            menu_id=menu_comment_model.menu_id,
            comment=menu_comment_model.comment,
            commented_at=menu_comment_model.commented_at
        )
        return menu_comment