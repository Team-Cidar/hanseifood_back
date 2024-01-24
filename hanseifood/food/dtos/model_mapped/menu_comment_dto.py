from datetime import datetime

from .user_dto import UserDto
from ..abstract_dto import Dto
from ...models import MenuComment


class MenuCommentDto(Dto):
    def __init__(self, user_dto: UserDto):
        self.comment_id: str = ''
        self.menu_id: str = ''
        self.user: UserDto = user_dto
        self.comment: str = ''
        self.commented_at: datetime = datetime.today()

    @classmethod
    def from_model(cls, menu_comment_model: MenuComment):
        menu_comment: MenuCommentDto = cls(
            user_dto=UserDto.from_model(menu_comment_model.user_id)
        )
        menu_comment.comment_id = str(menu_comment_model.comment_id)
        menu_comment.menu_id = str(menu_comment_model.menu_id)
        menu_comment.comment = str(menu_comment_model.comment)
        menu_comment.commented_at = menu_comment_model.commented_at
        return menu_comment