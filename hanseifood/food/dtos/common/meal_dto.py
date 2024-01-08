from ..abstract_dto import Dto
from ...models import Meal


class MealDto(Dto):
    def __init__(self):
        self.meal_name: str = ''

    @classmethod
    def from_model(cls, meal_model: Meal):
        meal: MealDto = cls()
        meal.meal_name = meal_model.meal_name
        return meal