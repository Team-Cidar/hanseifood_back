from django.http import HttpResponse, JsonResponse
from modules import excelParser
from .models import Day, Meal, DayMeal


def index(request):
    return HttpResponse("Hello world!")


# /student
def student_food_table(request):

## Day table생성
    file_path = "modules/test2.xlsx"  # 크롤링한 엑셀파일
    data = excelParser.ExcelParser.parse_excel(file_path)
    # response = JsonResponse(data, json_dumps_params={'ensure_ascii': False})

    for i in data.keys():
        test = Day(date=f"{i}")
        test.save()
    sample = Day.objects.first()
    response = sample.date

    # sample.delete()

    for i in data.values():
        print(i)

## 전체 삭제
    # response = 0
    # temp = Day.objects.all()
    # temp.delete()


## test
    # Day(date="")
    # test = Meal(meal_name='helllllllllllo')  # create
    # test.save()
    #
    # sample = Meal.objects.first()  # read
    # response = sample.meal_name
    # sample.delete()

    return HttpResponse(response)
