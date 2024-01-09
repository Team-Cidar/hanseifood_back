from django.db.models import QuerySet

from ..models import Meal
from ..repositories.abstract_repository import AbstractRepository


class MealRepository(AbstractRepository):
    def __init__(self):
        super(MealRepository, self).__init__(Meal.objects)

    def findByMenuName(self, menu_name) -> QuerySet:
        datas: QuerySet = self.manager.filter(meal_name=menu_name)
        return datas

    # override
    def save(self, meal_name) -> Meal:
        entity = Meal(meal_name=meal_name)
        entity.save()
        return entity
