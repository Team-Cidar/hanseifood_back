from django.db.models import QuerySet
from datetime import datetime
import openpyxl
from openpyxl.styles import Alignment
from openpyxl.workbook.workbook import Worksheet, Workbook
import logging
from typing import Dict, Union, List, Tuple

from .abstract_service import AbstractService
from ..core.utils import date_utils, os_utils
from ..dtos.daily_menu import DailyMenuDto
from ..models import Day
from ..repositories.day_repository import DayRepository
from ..repositories.daymeal_repository import DayMealRepository
from .menu_service import MenuService
from ..responses.objs.menu import MenuModel
from ..responses.objs.menu_modification import MenuModificationModel
from ..core.utils.string_utils import parse_str_to_list

logger = logging.getLogger(__name__)


class BackOfficeService(AbstractService):
    def __init__(self):
        # add repository instance variables
        self.__day_repository = DayRepository()
        self.__day_meal_repository = DayMealRepository()
        self.__menu_service = MenuService()

    def add_menus(self, data: Dict[str, Union[str, bool]]) -> MenuModificationModel:
        employee: List[str] = parse_str_to_list(data['employee'])
        student: List[str] = parse_str_to_list(data['student'])
        additional: List[str] = parse_str_to_list(data['additional'])

        date: datetime = datetime.strptime(data['datetime'], "%Y-%m-%d")
        day_model: QuerySet = self.__day_repository.findByDate(date=date)
        if not day_model.exists():  # first add
            daily_menu: DailyMenuDto = DailyMenuDto(date=date, student=student, employee=employee,
                                                    additional=additional)
            self.__menu_service.save_daily_menu(data=daily_menu)
            return MenuModificationModel(is_new=True)

        # modify menus
        day_model: Day = day_model[0]

        if len(additional) != 0:
            daymeal_models: QuerySet = self.__day_meal_repository.findAdditionalByDayId(day_id=day_model)
            self.__menu_service.delete_daily_menus(daymeal_models=daymeal_models)

        if len(student) != 0:
            daymeal_models: QuerySet = self.__day_meal_repository.findStudentByDayId(day_id=day_model)
            self.__menu_service.delete_daily_menus(daymeal_models=daymeal_models)

        if len(employee) != 0:
            daymeal_models: QuerySet = self.__day_meal_repository.findEmployeeByDayId(day_id=day_model)
            self.__menu_service.delete_daily_menus(daymeal_models=daymeal_models)

        daily_menu: DailyMenuDto = DailyMenuDto(date=day_model, student=student, employee=employee, additional=additional)
        self.__menu_service.save_daily_menu(data=daily_menu, is_update=True)

        self.__delete_excel_file(date=date)

        return MenuModificationModel(is_new=False)

    def get_excel_file(self, data: dict):
        date: datetime = datetime.strptime(data['date'], "%Y%m%d")

        weekly_menu: MenuModel = self.__menu_service.get_weekly_menu(date=date)
        file_name, exists = self.__check_excel_exists(date=date)
        if not exists:
            template: Workbook = openpyxl.load_workbook("assets/templates/excel_template.xlsx")
            sheet: Worksheet = template.active

            for idx, key in enumerate(weekly_menu.keys):
                col: str = chr(66 + idx)  # starts at B (B ~ F)
                sheet[f"{col}5"] = key
                sheet[f"{col}7"] = ',\n'.join(weekly_menu.employee_menu[key])
                sheet[f"{col}12"] = ',\n'.join(weekly_menu.student_menu[key])
                sheet[f"{col}17"] = ', '.join(weekly_menu.additional_menu[key])

                cell_format: Alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
                sheet[f"{col}7"].alignment = cell_format
                sheet[f"{col}12"].alignment = cell_format
                sheet[f"{col}17"].alignment = cell_format

            template.save(f"datas/{file_name}")

            template.close()

        return f"datas/{file_name}"

    def __check_excel_exists(self, date: datetime) -> Tuple[str, bool]:
        dates: List[str] = [item.strftime("%Y%m%d") for item in date_utils.get_dates_in_this_week(today=date)]
        file_name: str = f"{dates[0]}-{dates[-1]}.xlsx"
        return file_name, os_utils.check_file_exists(path="datas", file_name=file_name)

    def __delete_excel_file(self, date: datetime):
        file_name, exists = self.__check_excel_exists(date=date)
        if exists:
            os_utils.delete_file(f"datas/{file_name}")
