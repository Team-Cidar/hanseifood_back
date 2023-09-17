from typing import List, Tuple

from django.db.models import QuerySet

from ..dtos.day_meal import DayMealDto
from ..dtos.day import DayDto
from ..models import Day
from ..repositories.day_repository import DayRepository
from ..repositories.daymeal_repository import DayMealRepository
from ..core.utils import date_utils
from ..exceptions.menu_exceptions import EmptyDataError
from ..responses.objs.menu import MenuModel

import logging
import datetime

logger = logging.getLogger(__name__)


class MenuService:
    def __init__(self):
        self.__day_repository = DayRepository()
        self.__day_meal_repository = DayMealRepository()

    def get_one_day_menu(self) -> MenuModel:
        # return daily menu
        return self.get_target_days_menu(datetime.date.today())

    def get_this_week_menu(self) -> MenuModel:
        this_week: List[datetime] = date_utils.get_dates_in_this_week()

        response: MenuModel = MenuModel()

        date: datetime
        for date in this_week:
            day_meal_dtos: List[DayMealDto]
            today_dto: DayDto
            day_meal_dtos, today_dto = self.__get_day_n_daymeal(date)

            response += self.__get_daily_menu(today_dto.date, day_meal_dtos)

        return response

    def get_target_days_menu(self, date: datetime) -> MenuModel:
        date: datetime = date_utils.get_weekday(date)  # to get friday when today is 'sat' or 'sun'

        day_meal_dtos: List[DayMealDto]
        today_dto: DayDto
        day_meal_dtos, today_dto = self.__get_day_n_daymeal(date)

        response = self.__get_daily_menu(today_dto.date, day_meal_dtos)

        return response

    def __get_day_n_daymeal(self, date: datetime) -> Tuple[List[DayMealDto], DayDto]:
        day_models: QuerySet = self.__day_repository.findByDate(date)
        if day_models.count() == 0:
            raise EmptyDataError(f"Day model of [{date}] is not exists in database.")
        today: Day = day_models[0]

        day_meal_models: QuerySet = self.__day_meal_repository.findByDayId(today)
        if day_meal_models.count() == 0:
            raise EmptyDataError(f"DayMeal model of [{today}] is not exists in database.")

        day_meal_dtos: List[DayMealDto] = [item.to_dto() for item in day_meal_models]
        today_dto: DayDto = today.to_dto()

        return day_meal_dtos, today_dto

    @staticmethod
    def __get_daily_menu(date: datetime, today_meals: List[DayMealDto]) -> MenuModel:
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

        if len(student) != 0:
            result.student_menu[key] = student
            result.only_employee = False

        if len(additional) != 0:
            result.has_additional = True
            result.additional_menu[key] = additional  # for new template

        result.employee_menu[key] = employee

        return result
