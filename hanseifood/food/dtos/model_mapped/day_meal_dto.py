from .meal_dto import MealDto
from .day_dto import DayDto
from ..abstract_dto import Dto
from ...models import DayMeal


class DayMealDto(Dto):
    def __init__(self, day_dto: DayDto, meal_dto: MealDto):
        self.date: str = day_dto.date
        self.meal_name: str = meal_dto.meal_name
        self.for_student: bool = False
        self.is_additional: bool = False

    @classmethod
    def from_model(cls, day_meal_model: DayMeal):
        day_meal: DayMealDto = cls(
            day_dto=DayDto.from_model(day_meal_model.day_id),
            meal_dto=MealDto.from_model(day_meal_model.meal_id)
        )
        day_meal.for_student = day_meal_model.for_student
        day_meal.is_additional = day_meal_model.is_additional
        return day_meal