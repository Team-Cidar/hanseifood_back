from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from ..core.decorators.authentication_decorator import require_auth
from ..core.decorators.deserialize_decorator import deserialize
from ..dtos.requests.add_menu_request_dto import AddMenuRequestDto
from ..dtos.requests.get_excel_file_request_dto import GetExcelFileRequestDto
from ..dtos.responses.menu_modification_response_dto import MenuModificationResponseDto
from ..enums.role_enums import UserRole
from ..exceptions.type_exceptions import NotDtoClassError
from ..exceptions.request_exceptions import MissingFieldError, WeekendDateError, PastDateModificationError
from ..services.backoffice_service import BackOfficeService
from ..responses.error_response import ErrorResponse
from ..responses.dto_response import DtoResponse
from ..responses.file_response import FileResponse

backoffice_service: BackOfficeService = BackOfficeService()


# /back/menus POST
@api_view(['POST'])
@csrf_exempt
@require_auth([UserRole.ADMIN])
@deserialize
def add_menu(request: HttpRequest, data: AddMenuRequestDto) -> HttpResponse:
    try:
        response: MenuModificationResponseDto = backoffice_service.add_menus(data)
        if response.is_new:
            return DtoResponse.response(response, 201)
        return DtoResponse.response(response)
    except MissingFieldError as e:
        return ErrorResponse.response(e, 400)
    except WeekendDateError as e:
        return ErrorResponse.response(e, 400)
    except PastDateModificationError as e:
        return ErrorResponse.response(e, 400)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /back/menus/excel? GET
@api_view(['GET'])
@require_auth([UserRole.ADMIN])
@deserialize
def get_excel_file(request: HttpRequest, data: GetExcelFileRequestDto) -> HttpResponse:
    try:
        file_name = backoffice_service.get_excel_file(data)
        return FileResponse.response(file_path=file_name, content_type="application/vnd.ms-excel")
    except MissingFieldError as e:
        return ErrorResponse.response(e, 400)
    except Exception as e:
        return ErrorResponse.response(e, 500)
