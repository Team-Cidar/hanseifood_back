from datetime import datetime

from .menu_by_id_response_dto import MenuByIdResponseDto
from ..abstract_dto import Dto
from ..model_mapped.comment_deleted_dto import CommentDeletedDto
from ..model_mapped.menu_comment_dto import MenuCommentDto
from ..model_mapped.user_dto import UserDto


class CommenterDto(Dto):
    def __init__(self, user: UserDto):
        self.kakao_id = user.kakao_id
        self.nickname = user.nickname


class CommentResponseDto(Dto):
    def __init__(self, menu_comment_dto: MenuCommentDto, menu: MenuByIdResponseDto):
        self.comment_id: str = menu_comment_dto.comment_id
        self.menu: MenuByIdResponseDto = menu
        self.commenter: CommenterDto = CommenterDto(menu_comment_dto.user)
        self.comment: str = menu_comment_dto.comment
        self.commented_at: datetime = menu_comment_dto.commented_at
        self.deleted: bool = False


class DeletedCommentResponseDto(CommentResponseDto):
    def __init__(self, comment_deleted_dto: CommentDeletedDto, menu: MenuByIdResponseDto):
        super(DeletedCommentResponseDto, self).__init__(comment_deleted_dto, menu)
        self.deleted_at: datetime = comment_deleted_dto.deleted_at
        self.deleted = True