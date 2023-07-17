from django.http import HttpResponse, JsonResponse
from modules import excelParser
from .models import Day, Meal, DayMeal


def index(request):
    return HttpResponse("Hello world!")


# /student
def student_food_table(request):
    # file_path = "modules/test2.xlsx"  # 크롤링한 엑셀파일
    # data = excelParser.parse_students_menu(file_path)
    # response = JsonResponse(data, json_dumps_params={'ensure_ascii': False})

    test = Meal(meal_name='helllllllllllo')  # create
    test.save()

    sample = Meal.objects.first()  # read
    response = sample.meal_name
    sample.delete()

    return HttpResponse(response)
