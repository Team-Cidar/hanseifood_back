from django.http import HttpResponse, JsonResponse
from modules import excelParser


def index(request):
    return HttpResponse("Hello world!")


# /student
def student_food_table(request):
    file_path = "modules/test2.xlsx"  # 크롤링한 엑셀파일
    data = excelParser.parse_students_menu(file_path)
    response = JsonResponse(data, json_dumps_params={'ensure_ascii': False})
    return response
