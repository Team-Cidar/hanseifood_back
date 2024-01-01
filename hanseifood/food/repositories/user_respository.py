from django.db.models import QuerySet
from typing import Tuple

from .abstract_repository import AbstractRepository
from ..models import CustomUser


class UserRepository(AbstractRepository):
    def __init__(self):
        super(UserRepository, self).__init__(CustomUser.objects)

    def findByUsername(self, username: str) -> QuerySet:
        datas: QuerySet = self.model.filter(username=username)
        return datas

    def existsByUsername(self, username: str) -> Tuple[bool, QuerySet]:
        datas: QuerySet = self.findByUsername(username=username)
        return datas.exists(), datas

    # override
    def save(self, ) -> CustomUser:
        # entity = DayMeal(day_id=day_id, meal_id=meal_id, for_student=for_student, is_additional=is_additional)
        entity = CustomUser()
        entity.save()
        return entity
