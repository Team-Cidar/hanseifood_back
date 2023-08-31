import datetime
import logging

from ..exceptions.menu_exceptions import EmptyDataError
from ..models import Day, DayMeal
from ..objs.menu import MenuModel
from ..repositories.day_repository import DayRepository
from ..repositories.daymeal_repository import DayMealRepository

logger = logging.getLogger(__name__)

dayRepository = DayRepository()
dayMealRepository = DayMealRepository()


def get_daily_menu(date, response: MenuModel):
    try:
        day = date.weekday()
        if day in [5, 6]:  # [sat, sun]
            date -= datetime.timedelta(days=day - 4)  # get friday

        # today = Day.objects.filter(date=date)[0]  # get day obj of today in db
        today = dayRepository.findByDate(date)[0]
        # todays_meal = DayMeal.objects.filter(day_id=today)  # get today's menus in db
        todays_meal = dayMealRepository.findByDayId(today)

        student = []
        employee = []
        for item in todays_meal:
            if not item.for_student:
                employee.append(item.meal_id.meal_name)
            else:
                student.append(item.meal_id.meal_name)
                employee.append(item.meal_id.meal_name)
            # if item.for_student:
            #     response.student_menu.append(item.meal_id.meal_name)
            # else:
            #     response.employee_menu.append(item.meal_id.meal_name)

        if len(student) != 0:
            response.student_menu[str(today.date)] = student
        if len(employee) != 0:
            response.employee_menu[str(today.date)] = employee

        # if len(response.student_menu) == 0:
        #     response.only_employee = True

        # if len(response.employee_menu) > 1 and not response.only_employee:
        #     response.has_two_menus = True

        return response
    except EmptyDataError as e:
        logger.error(e)
        return response
    except Exception as e:
        logger.error(e)
        return response
