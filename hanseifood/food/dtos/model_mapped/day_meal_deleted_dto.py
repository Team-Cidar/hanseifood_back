from datetime import datetime

from .day_dto import DayDto
from .day_meal_dto import DayMealDto
from .meal_dto import MealDto
from ...enums.menu_enums import MenuType
from ...models import DayMeal, DayMealDeleted


class DayMealDeletedDto(DayMealDto):
    def __init__(self, day_dto: DayDto, meal_dto: MealDto, menu_type: MenuType, menu_id: str, deleted_at: datetime):
        super().__init__(
            day_dto=day_dto,
            meal_dto=meal_dto,
            menu_type=menu_type,
            menu_id=menu_id
        )
        self.deleted_at: datetime = deleted_at

    @classmethod
    def from_model(cls, menu_deleted_model: DayMealDeleted):
        dto: DayMealDeletedDto = cls(
            day_dto=DayDto.from_model(menu_deleted_model.day_id),
            meal_dto=MealDto.from_model(menu_deleted_model.meal_id),
            menu_type=MenuType.from_value(menu_deleted_model.menu_type),
            menu_id=str(menu_deleted_model.menu_id),
            deleted_at=menu_deleted_model.deleted_at
        )
        return dto