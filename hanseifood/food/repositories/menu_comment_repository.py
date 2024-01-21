from .abstract_repository import AbstractRepository
from ..models import MenuComment, User


class MenuCommentRepository(AbstractRepository):
    def __init__(self):
        super(MenuCommentRepository, self).__init__(MenuComment.objects)

    # override
    def save(self, menu_id: str, user_id: User, comment: str) -> MenuComment:
        entity: MenuComment = MenuComment(
            menu_id=menu_id,
            user_id=user_id,
            comment=comment
        )
        entity.save()
        return entity
