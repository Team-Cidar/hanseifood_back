from typing import Dict

from ..abstract_dto import Dto


class MenuResponseDto(Dto):
    def __init__(self, key: str = None):
        self.keys: list = [key] if key else []
        self.student_menu: MenuDto = MenuDto(key)
        self.employee_menu: MenuDto = MenuDto(key)
        self.additional_menu: MenuDto = MenuDto(key)

    def __add__(self, menus):
        menus: MenuResponseDto
        self.keys.extend(menus.keys)
        self.student_menu += menus.student_menu
        self.employee_menu += menus.employee_menu
        self.additional_menu += menus.additional_menu
        return self

    def add_employee(self, key: str, value: list):
        self.employee_menu.add_menus(key, value)

    def add_student(self, key: str, value: list):
        self.student_menu.add_menus(key, value)

    def add_additional(self, key: str, value: list):
        self.additional_menu.add_menus(key, value)

class MenuDto(Dto):
    def __init__(self, key: str = None):
        self.exists: bool = False
        self.menus: Dict[str, list] = {key: []} if key else {}

    def __add__(self, menu):
        menu: MenuDto
        self.exists |= menu.exists
        self.menus.update(menu.menus)
        return self

    def add_menus(self, key: str, values: list):
        self.menus[key] = values
        self.exists = True

    def get_menus(self, key: str) -> list:
        return self.menus[key]
