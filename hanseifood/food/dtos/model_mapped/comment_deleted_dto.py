from datetime import datetime

from .menu_comment_dto import MenuCommentDto
from .user_dto import UserDto
from ...models import CommentDeleted


class CommentDeletedDto(MenuCommentDto):
    def __init__(self,comment_id: str, menu_id: str, user_dto: UserDto, comment: str, commented_at: datetime, deleted_at: datetime):
        super().__init__(
            comment_id=comment_id,
            menu_id=menu_id,
            user_dto=user_dto,
            comment=comment,
            commented_at=commented_at
        )
        self.deleted_at: datetime = deleted_at

    @classmethod
    def from_model(cls, comment_deleted_model: CommentDeleted):
        dto: CommentDeletedDto = cls(
            comment_id=comment_deleted_model.comment_id,
            menu_id=comment_deleted_model.menu_id,
            user_dto=UserDto.from_model(comment_deleted_model.user_id),
            comment=comment_deleted_model.comment,
            commented_at=comment_deleted_model.commented_at,
            deleted_at=comment_deleted_model.deleted_at
        )
        return dto