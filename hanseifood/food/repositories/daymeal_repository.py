from typing import Tuple
from django.db.models import QuerySet

from .abstract_repository import AbstractRepository
from ..enums.menu_enums import MenuType
from ..models import DayMeal, Day, Meal


class DayMealRepository(AbstractRepository):
    def __init__(self):
        super(DayMealRepository, self).__init__(DayMeal.objects)

    def findByDayId(self, day_id: Day) -> QuerySet:
        datas: QuerySet = self.manager.filter(day_id=day_id)
        return datas

    def findByDayIdAndMenuType(self, day_id: Day, menu_type: MenuType) -> QuerySet:
        datas: QuerySet = self.manager.filter(day_id=day_id, menu_type=menu_type.value)
        return datas

    def existByDayIdAndMenuType(self, day_id: Day, menu_type: MenuType) -> Tuple[bool, QuerySet]:
        datas: QuerySet = self.findByDayIdAndMenuType(day_id=day_id, menu_type=menu_type)
        return datas.exists(), datas

    def deleteByDayIdAndMenuType(self, day_id: Day, menu_type: MenuType):
        item: DayMeal
        for item in self.findByDayIdAndMenuType(day_id=day_id, menu_type=menu_type):
            item.delete()  # do not delete DayMeal record with queryset.delete() to call overriden delete method

    # override
    def save(self, day_id: Day, meal_id: Meal, menu_type: MenuType, menu_id: str) -> DayMeal:
        entity = DayMeal(day_id=day_id, meal_id=meal_id, menu_type=menu_type.value, menu_id=menu_id)
        entity.save()
        return entity
