from .meal_dto import MealDto
from .day_dto import DayDto
from ..abstract_dto import Dto
from ...enums.menu_enums import MenuType
from ...models import DayMeal


class DayMealDto(Dto):
    def __init__(self, day_dto: DayDto, meal_dto: MealDto):
        self.day_dto: DayDto = day_dto
        self.meal_dto: MealDto = meal_dto
        self.menu_type: MenuType = MenuType.NONE
        self.menu_id: str = ''

    @classmethod
    def from_model(cls, day_meal_model: DayMeal):
        day_meal: DayMealDto = cls(
            day_dto=DayDto.from_model(day_meal_model.day_id),
            meal_dto=MealDto.from_model(day_meal_model.meal_id)
        )
        day_meal.menu_type = MenuType.from_value(str(day_meal_model.menu_type))
        day_meal.menu_id = str(day_meal_model.menu_id)
        return day_meal