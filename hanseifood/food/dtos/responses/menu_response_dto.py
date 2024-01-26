from datetime import datetime
from typing import Dict, List

from ..abstract_dto import Dto
from ..model_mapped.day_meal_deleted_dto import DayMealDeletedDto
from ..model_mapped.day_meal_dto import DayMealDto
from ...enums.menu_enums import MenuType
from ...exceptions.type_exceptions import DefaultEnumTypeError, OperateDifferentTypesError


class MenuDto(Dto):
    def __init__(self, day_meal_dto: DayMealDto=None, deleted: bool=False):
        if day_meal_dto:
            self.menu: List[str] = [day_meal_dto.meal_dto.meal_name]
            self.menu_id: str = day_meal_dto.menu_id
            self.menu_type: MenuType = day_meal_dto.menu_type
        else:
            self.menu = []
            self.menu_id = ''
            self.menu_type = MenuType.NONE
        self.like_count: int = 0
        self.comment_count: int = 0
        self.deleted: bool = deleted

    def __add__(self, menu_dto):
        menu_dto: MenuDto
        if self.menu_type == MenuType.NONE:
            return menu_dto
        elif self.menu_type == menu_dto.menu_type:
            self.menu.extend(menu_dto.menu)
            return self
        else:
            raise OperateDifferentTypesError(f"Cannot add menus from type '{menu_dto.menu_type}' to '{self.menu_type}'")


class MenuDeletedDto(MenuDto):
    def __init__(self, menu_deleted_dto: DayMealDeletedDto=None):
        super(MenuDeletedDto, self).__init__(menu_deleted_dto, True)
        self.deleted_at: datetime = menu_deleted_dto.deleted_at


class MenuSetDto(Dto):
    def __init__(self, key: str = None):
        self.exists: bool = False
        self.menus: Dict[str, MenuDto] = {key: MenuDto()} if key else {}

    def __add__(self, menu):
        menu: MenuSetDto
        self.exists |= menu.exists
        self.menus.update(menu.menus)
        return self

    def add_menus(self, key: str, day_meal_dtos: List[DayMealDto], like_count: int, comment_count: int):
        menu_dto: MenuDto = MenuDto()
        for day_meal in day_meal_dtos:
            menu_dto += MenuDto(day_meal)
        menu_dto.like_count = like_count
        menu_dto.comment_count = comment_count

        self.menus[key] = menu_dto
        self.exists = True

    def get_menus(self, key: str) -> list:
        return self.menus[key].menu


class MenuResponseDto(Dto):
    def __init__(self, key: str = None):
        self.keys: list = [key] if key else []
        self.student_menu: MenuSetDto = MenuSetDto(key)
        self.employee_menu: MenuSetDto = MenuSetDto(key)
        self.additional_menu: MenuSetDto = MenuSetDto(key)

    def __add__(self, menus):
        menus: MenuResponseDto
        self.keys.extend(menus.keys)
        self.student_menu += menus.student_menu
        self.employee_menu += menus.employee_menu
        self.additional_menu += menus.additional_menu
        return self

    def add_menus_by_type(self, _type: MenuType, date_key: str, day_meal_dtos: List[DayMealDto], like_count: int, comment_count: int):
        if _type == MenuType.EMPLOYEE:
            self.employee_menu.add_menus(date_key, day_meal_dtos, like_count, comment_count)
        elif _type == MenuType.STUDENT:
            self.student_menu.add_menus(date_key, day_meal_dtos, like_count, comment_count)
        elif _type == MenuType.ADDITIONAL:
            self.additional_menu.add_menus(date_key, day_meal_dtos, like_count, comment_count)
        else:
            raise DefaultEnumTypeError()

