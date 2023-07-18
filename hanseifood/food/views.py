import datetime

from django.http import HttpResponse, JsonResponse
from .models import Day, Meal, DayMeal
from .response_objs.menuResponse import MenuResponse


def index(request):
    return HttpResponse("Hello world!")


# /menus GET
def get_menu(request):
    today = Day.objects.filter(date=datetime.datetime.today())[0]  # get day obj of today in db
    todays_meal = DayMeal.objects.filter(day_id=today)  # get today's menus in db

    response = MenuResponse(today.date)

    for item in todays_meal:
        if item.for_student:
            response.student_menu.append(item.meal_id.meal_name)
        else:
            response.employee_menu.append(item.meal_id.meal_name)

    if len(response.student_menu) == 0:
        response.only_employee = True

    if len(response.employee_menu) > 1 and not response.only_employee:
        response.has_two_menus = True

    response_json = response.toJson()

    return HttpResponse(response_json)