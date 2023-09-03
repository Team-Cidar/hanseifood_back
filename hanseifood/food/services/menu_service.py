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

    def get_one_day_menu(self):
        # return daily menu
        try:
            date = date_utils.get_weekday(datetime.date.today())  # to get friday when today is 'sat' or 'sun'

            today = self.__day_repository.findByDate(date)[0]
            today_meals = self.__day_meal_repository.findByDayId(today)

            today_meals = [item.to_dto() for item in today_meals]
            today = today.to_dto()

            response = self.__get_daily_menu(today.date, today_meals)

            return response
        except EmptyDataError as e:
            logger.error(e)
            return response
        except Exception as e:
            logger.error(e)
            return response

    def get_this_week_menu(self):
        try:
            this_week = date_utils.get_dates_in_this_week()

            response = MenuModel()
            for date in this_week:
                today = self.__day_repository.findByDate(date)[0]
                today_meals = self.__day_meal_repository.findByDayId(today)

                today_meals = [item.to_dto() for item in today_meals]
                today = today.to_dto()

                response += self.__get_daily_menu(today.date, today_meals)

            return response
        except EmptyDataError as e:
            logger.error(e)
            return response
        except Exception as e:
            logger.error(e)
            return response

    @staticmethod
    def __get_daily_menu(date, today_meals):
        student = []
        employee = []
        additional = []
        for item in today_meals:
            if item.for_student:
                student.append(item.meal_name)
            elif item.is_additional:  # for new template
                additional.append(item.meal_name)
            else:
                employee.append(item.meal_name)

        # if len(employee) <= 1:
        #     employee = student + employee

        result = MenuModel()

        if len(student) != 0:
            result.student_menu[str(date)] = student
            result.only_employee = False

        if len(additional) != 0:
            result.has_additional = True
            result.additional_menu[str(date)] = additional  # for new template

        result.employee_menu[str(date)] = employee

        return result
