from django.db.models import QuerySet
from typing import Tuple

from .abstract_repository import AbstractRepository
from ..models import User


class UserRepository(AbstractRepository):
    def __init__(self):
        super(UserRepository, self).__init__(User.objects)

    def findByUsername(self, username: str) -> QuerySet:
        datas: QuerySet = self.model.filter(username=username)
        return datas

    def existsByUsername(self, username: str) -> Tuple[bool, QuerySet]:
        datas: QuerySet = self.findByUsername(username=username)
        return datas.exists(), datas

    # override
    def save(self, ) -> User:
        # entity = DayMeal(day_id=day_id, meal_id=meal_id, for_student=for_student, is_additional=is_additional)
        entity = User()
        entity.save()
        return entity
