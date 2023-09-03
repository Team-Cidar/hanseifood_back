from typing import List
from django.db.models import Model, QuerySet

from .abstract_repository import AbstractRepository
from ..exceptions.menu_exceptions import EmptyDataError
from ..models import DayMeal, Day


class DayMealRepository(AbstractRepository):
    def __init__(self):
        super().__init__(DayMeal.objects)

    def findByDayId(self, day_id: Day) -> QuerySet:
        datas: QuerySet = self.model.filter(day_id=day_id)
        # if not datas.exists():
        #     raise EmptyDataError(f"{day_id.date}'s meal data is not exists")
        return datas

    # override
    def save(self, day_id, meal_id, for_student, is_additional) -> Model:
        entity = DayMeal(day_id=day_id, meal_id=meal_id, for_student=for_student, is_additional=is_additional)
        entity.save()
        return entity
