from datetime import datetime

from ..abstract_dto import Dto
from ..model_mapped.comment_deleted_dto import CommentDeletedDto
from ..model_mapped.menu_comment_dto import MenuCommentDto
from ..model_mapped.user_dto import UserDto


class CommenterDto(Dto):
    def __init__(self, user: UserDto):
        self.kakao_id = user.kakao_id
        self.nickname = user.nickname


class CommentResponseDto(Dto):
    def __init__(self, menu_comment_dto: MenuCommentDto, deleted: bool=False):
        self.comment_id: str = menu_comment_dto.comment_id
        self.menu_id: str = menu_comment_dto.menu_id
        self.commenter: CommenterDto = CommenterDto(menu_comment_dto.user)
        self.comment: str = menu_comment_dto.comment
        self.commented_at: datetime = menu_comment_dto.commented_at
        self.deleted: bool = deleted


class DeletedCommentResponseDto(CommentResponseDto):
    def __init__(self, comment_deleted_dto: CommentDeletedDto):
        super(DeletedCommentResponseDto, self).__init__(comment_deleted_dto, True)
        self.deleted_at: datetime = comment_deleted_dto.deleted_at