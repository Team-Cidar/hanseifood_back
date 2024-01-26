from typing import Tuple

from django.db.models import QuerySet

from .abstract_repository import AbstractRepository
from ..models import MenuComment, User, MenuLike


class MenuLikeRepository(AbstractRepository):
    def __init__(self):
        super(MenuLikeRepository, self).__init__(MenuLike.objects)

    def findByMenuIdAndUserId(self, menu_id: str, user_id: User) -> QuerySet:
        data: QuerySet = self.manager.filter(menu_id=menu_id, user_id=user_id)
        return data

    def findByMenuId(self, menu_id: str) -> QuerySet:
        data: QuerySet = self.manager.filter(menu_id=menu_id)
        return data

    def findByUserId(self, user_id: User) -> QuerySet:
        data: QuerySet = self.manager.filter(user_id=user_id)
        return data

    def existByMenuIdAndUserId(self, menu_id: str, user_id: User) -> Tuple[bool, QuerySet]:
        data: QuerySet = self.findByMenuIdAndUserId(menu_id=menu_id, user_id=user_id)
        return data.exists(), data

    def existByUserId(self, user_id: User) -> Tuple[bool, QuerySet]:
        data: QuerySet = self.findByUserId(user_id=user_id)
        return data.exists(), data

    def countByMenuId(self, menu_id: str) -> int:
        return self.findByMenuId(menu_id=menu_id).count()

    # override
    def save(self, menu_id: str, user_id: User) -> MenuLike:
        entity: MenuLike = MenuLike(
            menu_id=menu_id,
            user_id=user_id,
        )
        entity.save()
        return entity
