
from django.http import HttpResponse, JsonResponse
from modules import excelParser


def index(request):
    return HttpResponse("Hello world!")

def student_food_table(request):
    file_path = "modules/test1.xlsx"
    data = excelParser.parse_students_menu(file_path)
    response = JsonResponse(data, json_dumps_params={'ensure_ascii': False})
    return response
