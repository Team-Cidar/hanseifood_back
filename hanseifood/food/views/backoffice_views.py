from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from ..core.decorators.authentication_decorator import require_auth
from ..core.decorators.deserialize_decorator import deserialization
from ..core.utils.request_utils import extract_request_datas
from ..dtos.add_menu_request_dto import AddMenuRequestDto
from ..enums.role_enums import UserRole
from ..exceptions.type_exceptions import NotAbstractModelError
from ..exceptions.request_exceptions import MissingFieldError
from ..services.backoffice_service import BackOfficeService
from ..responses.objs.menu_modification import MenuModificationModel
from ..responses.error_response import ErrorResponse
from ..responses.model_response import ModelResponse
from ..responses.file_response import FileResponse

backoffice_service: BackOfficeService = BackOfficeService()


# /back/menus POST
@api_view(['POST'])
@csrf_exempt
@require_auth([UserRole.A])
@deserialization(AddMenuRequestDto)
def add_menu(request: HttpRequest) -> HttpResponse:
    try:
        data: tuple = extract_request_datas(request.data, ['employee', 'student', 'additional', 'datetime'])
        response: MenuModificationModel = backoffice_service.add_menus(data)
        if response.is_new:
            return ModelResponse.response(response, 201)
        return ModelResponse.response(response)
    except MissingFieldError as e:
        return ErrorResponse.response(e, 400)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /back/menus/excel? GET
@api_view(['GET'])
@require_auth([UserRole.A])
def get_excel_file(request: HttpRequest) -> HttpResponse:
    try:
        date: str = extract_request_datas(request.GET, ['date'])
        file_name = backoffice_service.get_excel_file(date)
        return FileResponse.response(file_path=file_name, content_type="application/vnd.ms-excel")
    except MissingFieldError as e:
        return ErrorResponse.response(e, 400)
    except Exception as e:
        return ErrorResponse.response(e, 500)
