from datetime import datetime
from typing import Tuple

from django.db.models import QuerySet

from .abstract_repository import AbstractRepository
from ..models import User, CommentDeleted


class CommentDeletedRepository(AbstractRepository):
    def __init__(self):
        super(CommentDeletedRepository, self).__init__(CommentDeleted.objects)

    def findByCommentId(self, comment_id: str) -> QuerySet:
        data: QuerySet = self.manager.filter(comment_id=comment_id)
        return data

    def existByCommentId(self, comment_id: str) -> Tuple[bool, QuerySet]:
        data: QuerySet = self.findByCommentId(comment_id)
        return data.exists(), data

    # override
    def save(self, comment_id: str, menu_id: str, commenter: User, comment: str, commented_at: datetime) -> CommentDeleted:
        entity: CommentDeleted = CommentDeleted(
            comment_id=comment_id,
            menu_id=menu_id,
            user_id=commenter,
            comment=comment,
            commented_at=commented_at
        )
        entity.save()
        return entity
