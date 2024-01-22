from typing import Tuple

from django.db.models import QuerySet

from .abstract_repository import AbstractRepository
from ..models import MenuComment, User


class MenuCommentRepository(AbstractRepository):
    def __init__(self):
        super(MenuCommentRepository, self).__init__(MenuComment.objects)

    def findByMenuId(self, menu_id: str) -> QuerySet:
        data: QuerySet = self.manager.filter(menu_id=menu_id)
        return data

    def existByMenuId(self, menu_id: str) -> Tuple[bool, QuerySet]:
        data: QuerySet = self.findByMenuId(menu_id=menu_id)
        return data.exists(), data

    def findByUserId(self, user_id: User) -> QuerySet:
        data: QuerySet = self.manager.filter(user_id=user_id)
        return data

    def findByCommentId(self, comment_id: int) -> QuerySet:
        comment: QuerySet = self.manager.filter(comment_id=comment_id)
        return comment

    def existByCommentId(self, comment_id: int) -> Tuple[bool, QuerySet]:
        comment: QuerySet = self.findByCommentId(comment_id=comment_id)
        return comment.exists(), comment

    def delete(self, comment: MenuComment):
        comment.delete()

    # override
    def save(self, menu_id: str, user_id: User, comment: str) -> MenuComment:
        entity: MenuComment = MenuComment(
            menu_id=menu_id,
            user_id=user_id,
            comment=comment
        )
        entity.save()
        return entity
