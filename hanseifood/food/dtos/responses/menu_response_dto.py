from typing import Dict, List

from ..abstract_dto import Dto
from ..model_mapped.day_meal_dto import DayMealDto
from ...enums.menu_enums import MenuType
from ...exceptions.type_exceptions import DefaultEnumTypeError


class MenuDto(Dto):
    def __init__(self):
        self.menu: List[str] = list()
        self.menu_id: str = ''


class MenuSetDto(Dto):
    def __init__(self, key: str = None):
        self.exists: bool = False
        self.menus: Dict[str, MenuDto] = {key: MenuDto()} if key else {}

    def __add__(self, menu):
        menu: MenuSetDto
        self.exists |= menu.exists
        self.menus.update(menu.menus)
        return self

    def add_menus(self, key: str, day_meal_dtos: List[DayMealDto]):
        menu_dto: MenuDto = MenuDto()
        menu_dto.menu = [dto.meal_dto.meal_name for dto in day_meal_dtos]
        menu_dto.menu_id = day_meal_dtos[0].menu_id
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

    def add_menus_by_type(self, _type: MenuType, date_key: str, day_meal_dtos: List[DayMealDto]):
        if _type == MenuType.EMPLOYEE:
            self.employee_menu.add_menus(date_key, day_meal_dtos)
        elif _type == MenuType.STUDENT:
            self.student_menu.add_menus(date_key, day_meal_dtos)
        elif _type == MenuType.ADDITIONAL:
            self.additional_menu.add_menus(date_key, day_meal_dtos)
        else:
            raise DefaultEnumTypeError()

