from django.db.models import Model, QuerySet

from ..models import Meal
from ..repositories.abstract_repository import AbstractRepository
from ..exceptions.menu_exceptions import EmptyDataError


class MealRepository(AbstractRepository):
    def __init__(self):
        super().__init__(Meal.objects)

    def findByMenuName(self, menu_name) -> QuerySet:
        datas: QuerySet = self.model.filter(meal_name=menu_name)
        # if not datas.exists():
        #     raise EmptyDataError(f"{menu_name} data is not exists")
        return datas

    # override
    def save(self, meal_name) -> Model:
        entity = Meal(meal_name=meal_name)
        entity.save()
        return entity
