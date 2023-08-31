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

        today = dayRepository.findByDate(date)[0]
        todays_meal = dayMealRepository.findByDayId(today)

        student = []
        employee = []
        for item in todays_meal:
            if item.for_student:
                student.append(item.meal_id.meal_name)
            else:
                employee.append(item.meal_id.meal_name)

        if len(employee) <= 1:
            employee = student + employee

        if len(student) != 0:
            response.student_menu[str(today.date)] = student
        response.employee_menu[str(today.date)] = employee

        return response
    except EmptyDataError as e:
        logger.error(e)
        return response
    except Exception as e:
        logger.error(e)
        return response
