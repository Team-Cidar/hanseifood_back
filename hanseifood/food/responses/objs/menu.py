from datetime import datetime

from typing import Dict

from .abstract_model import AbstractModel
from ...core.constants.strings.menu_strings import MENU_NOT_EXISTS
from ...core.utils import date_utils


class MenuModel(AbstractModel):
    def __init__(self):
        self.only_employee = True
        self.has_additional = False
        self.student_menu: Dict[str, list] = dict()
        self.employee_menu: Dict[str, list] = dict()
        self.additional_menu: Dict[str, list] = dict()

    def add_empty_date(self, date: datetime):
        date_str = date.strftime("%Y-%m-%d")
        weekday_kor: str = date_utils.get_weekday_kor(date_str)

        key: str = f'{str(date)} ({weekday_kor})'
        self.student_menu[key] = [MENU_NOT_EXISTS]
        self.employee_menu[key] = [MENU_NOT_EXISTS]
        self.additional_menu[key] = [MENU_NOT_EXISTS]

    # override
    def __add__(self, model):
        self.student_menu.update(model.student_menu)
        self.employee_menu.update(model.employee_menu)
        self.additional_menu.update(model.additional_menu)
        self.has_additional |= model.has_additional
        self.only_employee &= model.only_employee
        return self

    # override
    def _AbstractModel__serialize(self) -> dict:  # 추상 메서드가 private이라 재정의 할 때 _추상클래스__method() 이런식으로 해줘야함
        return {
            'only_employee': self.only_employee,
            'has_additional': self.has_additional,
            'student_menu': self.student_menu,
            'employee_menu': self.employee_menu,
            'additional_menu': self.additional_menu
        }