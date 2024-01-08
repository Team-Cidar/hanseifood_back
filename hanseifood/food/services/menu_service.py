from django.db.models import QuerySet
from datetime import datetime
import logging
from typing import List

from .abstract_service import AbstractService
from ..core.utils import date_utils
from ..dtos.model_mapped.day_meal_dto import DayMealDto
from ..dtos.general.daily_menu import DailyMenuDto
from ..dtos.responses.menu_response_dto import MenuResponseDto
from ..repositories.day_repository import DayRepository
from ..repositories.daymeal_repository import DayMealRepository
from ..repositories.meal_repository import MealRepository
from ..models import Day

logger = logging.getLogger(__name__)


class MenuService(AbstractService):
    def __init__(self):
        self.__day_repository = DayRepository()
        self.__day_meal_repository = DayMealRepository()
        self.__meal_repository = MealRepository()

    def get_today_menu(self) -> MenuResponseDto:
        return self.get_target_days_menu(datetime.today())

    def get_weekly_menu(self, date: datetime = datetime.today()) -> MenuResponseDto:
        this_week: List[datetime] = date_utils.get_dates_in_this_week(today=date)

        response: MenuResponseDto = MenuResponseDto()

        date: datetime
        for date in this_week:
            response += self.__get_daily_menus(date=date)

        return response

    def get_target_days_menu(self, date: datetime) -> MenuResponseDto:
        date = date_utils.get_weekday(date)  # to get friday when today is 'sat' or 'sun'
        return self.__get_daily_menus(date=date)

    def save_daily_menu(self, data: DailyMenuDto, is_update: bool = False) -> None:
        students: list = data.student
        employees: list = data.employee
        additional: list = data.additional

        day_model: Day
        if not is_update:
            day_model = self.__day_repository.save(data.date)
        else:
            day_model = data.date

        self.__save_daily_menus_to_db(day_model=day_model, datas=students, for_students=True, is_additional=False)
        self.__save_daily_menus_to_db(day_model=day_model, datas=employees, for_students=False, is_additional=False)
        self.__save_daily_menus_to_db(day_model=day_model, datas=additional, for_students=False, is_additional=True)

    def delete_daily_menus(self, daymeal_models: QuerySet):
        for model in daymeal_models:
            self.__day_meal_repository.delete(target_model=model)

    def __save_daily_menus_to_db(self, day_model, datas: list, for_students: bool, is_additional: bool):
        for menu in datas:
            menu_model = self.__meal_repository.findByMenuName(menu)
            if not menu_model.exists():
                menu_model = self.__meal_repository.save(menu)
            else:
                menu_model = menu_model[0]

            self.__day_meal_repository.save(day_id=day_model, meal_id=menu_model, for_student=for_students,
                                            is_additional=is_additional)

    def __get_daily_menus(self, date: datetime) -> MenuResponseDto:
        weekday_kor: str = date_utils.get_weekday_kor(date)
        key: str = f'{date.strftime("%Y-%m-%d")} ({weekday_kor})'

        result: MenuResponseDto = MenuResponseDto(key)

        day_model: QuerySet = self.__day_repository.findByDate(date=date)
        if not day_model.exists():
            return result

        day_model: Day = day_model[0]

        exists, employee_menu = self.__day_meal_repository.existEmployeeByDayId(day_id=day_model)
        if exists:
            result.add_employee(key, [DayMealDto.from_model(item).meal_name for item in employee_menu])

        exists, students_menu = self.__day_meal_repository.existStudentByDayId(day_id=day_model)
        if exists:
            result.add_student(key, [DayMealDto.from_model(item).meal_name for item in students_menu])

        exists, additional_menu = self.__day_meal_repository.existAdditionalByDayId(day_id=day_model)
        if exists:
            result.add_additional(key, [DayMealDto.from_model(item).meal_name for item in additional_menu])

        return result
