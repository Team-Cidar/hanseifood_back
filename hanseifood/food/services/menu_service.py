from typing import List, Tuple, Union

from django.db.models import QuerySet
import logging
from datetime import datetime

from ..core.constants.strings.menu_strings import MENU_NOT_EXISTS
from ..dtos.daily_menu import DailyMenuDto
from ..dtos.day_meal import DayMealDto
from ..dtos.day import DayDto
from ..models import Day
from ..repositories.day_repository import DayRepository
from ..repositories.daymeal_repository import DayMealRepository
from ..repositories.meal_repository import MealRepository
from ..core.utils import date_utils
from ..responses.objs.menu import MenuModel
from .abstract_service import AbstractService

logger = logging.getLogger(__name__)


class MenuService(AbstractService):
    def __init__(self):
        self.__day_repository = DayRepository()
        self.__day_meal_repository = DayMealRepository()
        self.__meal_repository = MealRepository()

    def get_one_day_menu(self) -> MenuModel:
        # return daily menu
        return self.get_target_days_menu(datetime.today())

    def get_weekly_menu(self, date: datetime = datetime.today()) -> MenuModel:
        # return weekly menu
        this_week: List[datetime] = date_utils.get_dates_in_this_week(today=date)

        response: MenuModel = MenuModel()

        date: datetime
        for date in this_week:
            day_meal_dtos: List[DayMealDto]
            today_dto: DayDto
            day_meal_dtos, today_dto = self.__get_day_n_daymeal(date)
            if today_dto is None:
                response.add_empty_date(date)
                continue

            response += self.__get_daily_menu(today_dto.date, day_meal_dtos)

        return response

    def get_target_days_menu(self, date: datetime) -> MenuModel:
        date: datetime = date_utils.get_weekday(date)  # to get friday when today is 'sat' or 'sun'

        day_meal_dtos: List[DayMealDto]
        today_dto: DayDto
        day_meal_dtos, today_dto = self.__get_day_n_daymeal(date)
        if today_dto is None:
            response: MenuModel = MenuModel()
            response.add_empty_date(date)
        else:
            response = self.__get_daily_menu(today_dto.date, day_meal_dtos)

        return response

    def save_daily_menu(self, data: DailyMenuDto) -> None:
        students: list = data.student
        employees: list = data.employee
        additional: list = data.additional

        day_model = self.__day_repository.save(data.date)

        self.save_to_db(day_model=day_model, datas=students, for_students=True, is_additional=False)
        self.save_to_db(day_model=day_model, datas=employees, for_students=False, is_additional=False)
        self.save_to_db(day_model=day_model, datas=additional, for_students=False, is_additional=True)

    def save_to_db(self, day_model, datas: list, for_students: bool, is_additional: bool):
        for menu in datas:
            menu_model = self.__meal_repository.findByMenuName(menu)
            if not menu_model.exists():
                menu_model = self.__meal_repository.save(menu)
            else:
                menu_model = menu_model[0]

            self.__day_meal_repository.save(day_id=day_model, meal_id=menu_model, for_student=for_students,
                                            is_additional=is_additional)

    def __get_day_n_daymeal(self, date: datetime) -> Union[Tuple[list, None], Tuple[List[DayMealDto], DayDto]]:
        day_models: QuerySet = self.__day_repository.findByDate(date)
        if day_models.count() == 0:
            return [], None
        today: Day = day_models[0]

        day_meal_models: QuerySet = self.__day_meal_repository.findByDayId(today)
        if day_meal_models.count() == 0:
            return [], None

        day_meal_dtos: List[DayMealDto] = [item.to_dto() for item in day_meal_models]
        today_dto: DayDto = today.to_dto()

        return day_meal_dtos, today_dto

    def __get_daily_menu(self, date: datetime, today_meals: List[DayMealDto]) -> MenuModel:
        student: list = []
        employee: list = []
        additional: list = []

        item: DayMealDto
        for item in today_meals:
            if item.for_student:
                student.append(item.meal_name)
            elif item.is_additional:
                additional.append(item.meal_name)
            else:
                employee.append(item.meal_name)

        result: MenuModel = MenuModel()

        weekday_kor: str = date_utils.get_weekday_kor(date)

        key: str = f'{str(date)} ({weekday_kor})'

        result.keys.append(key)

        if len(student) != 0:
            result.student_menu[key] = student
            result.only_employee = False
        else:
            result.student_menu[key] = [MENU_NOT_EXISTS]

        if len(additional) != 0:
            result.has_additional = True
            result.additional_menu[key] = additional  # for new template
        else:
            result.additional_menu[key] = [MENU_NOT_EXISTS]

        result.employee_menu[key] = employee

        return result
