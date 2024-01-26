from typing import Tuple
from django.db.models import QuerySet

from .abstract_repository import AbstractRepository
from ..enums.menu_enums import MenuType
from ..models import DayMeal, Day, Meal, DayMealDeleted


class DayMealDeletedRepository(AbstractRepository):
    def __init__(self):
        super(DayMealDeletedRepository, self).__init__(DayMealDeleted.objects)

    def findByMenuId(self, menu_id: str) -> QuerySet:
        data: QuerySet = self.manager.filter(menu_id=menu_id)
        return data

    def findByDayIdAndMenuType(self, day_id: Day, menu_type: MenuType) -> QuerySet:
        data: QuerySet = self.manager.filter(day_id=day_id, menu_type=menu_type)
        return data

    def existByMenuId(self, menu_id: str) -> Tuple[bool, QuerySet]:
        data: QuerySet = self.findByMenuId(menu_id)
        return data.exists(), data

    # override
    def save(self, day_id: Day, meal_id: Meal, menu_type: MenuType, menu_id: str) -> DayMealDeleted:
        entity = DayMealDeleted(
            day_id=day_id,
            meal_id=meal_id,
            menu_type=menu_type.value,
            menu_id=menu_id
        )
        entity.save()
        return entity
