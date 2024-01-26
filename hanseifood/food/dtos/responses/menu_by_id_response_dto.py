from datetime import datetime
from typing import List

from ..abstract_dto import Dto
from ..model_mapped.day_meal_deleted_dto import DayMealDeletedDto
from ..model_mapped.day_meal_dto import DayMealDto
from ...enums.menu_enums import MenuType


class MenuByIdResponseDto(Dto):
    def __init__(self, day_meal_dtos: List[DayMealDto], like_count: int, comment_count: int):
        day_meal_dto: DayMealDto = day_meal_dtos[0]
        self.date: str = day_meal_dto.day_dto.date
        self.menus: List[str] = [dto.meal_dto.meal_name for dto in day_meal_dtos]
        self.menu_id: str = day_meal_dto.menu_id
        self.menu_type: MenuType = day_meal_dto.menu_type
        self.like_count: int = like_count
        self.comment_count: int = comment_count
        self.deleted: bool = False


class DeletedMenuByIdResponseDto(MenuByIdResponseDto):
    def __init__(self, deleted_menu_dtos: List[DayMealDeletedDto], like_count: int, comment_count: int):
        super().__init__(deleted_menu_dtos, like_count, comment_count)
        self.deleted_at: datetime = deleted_menu_dtos[-1].deleted_at
        self.deleted = True