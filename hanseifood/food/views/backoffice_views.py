from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view

from ..core.decorators.authentication_decorator import require_auth
from ..core.decorators.deserialize_decorator import deserialize
from ..core.decorators.multi_method_decorator import multi_methods
from ..dtos.requests.add_menu_request_dto import AddMenuRequestDto
from ..dtos.requests.delete_menu_request_dto import DeleteMenuRequestDto
from ..dtos.requests.get_excel_file_request_dto import GetExcelFileRequestDto
from ..dtos.requests.get_menu_history_request_dto import GetMenuHistoryRequestDto
from ..dtos.requests.modify_user_role_request_dto import ModifyUserRoleRequestDto
from ..dtos.responses.common_status_response_dto import CommonStatusResponseDto
from ..dtos.responses.menu_modification_response_dto import MenuModificationResponseDto
from ..enums.role_enums import UserRole
from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.jwt_exceptions import PermissionDeniedError
from ..exceptions.type_exceptions import NotDtoClassError
from ..exceptions.request_exceptions import WeekendDateError, PastDateModificationError
from ..models import User
from ..services.backoffice_service import BackOfficeService
from ..responses.error_response import ErrorResponse
from ..responses.dto_response import DtoResponse
from ..responses.file_response import FileResponse

backoffice_service: BackOfficeService = BackOfficeService()


# /back/menus POST
@require_auth([UserRole.ADMIN, UserRole.MANAGER])
@deserialize
def add_menu(request: HttpRequest, data: AddMenuRequestDto) -> HttpResponse:
    try:
        response: MenuModificationResponseDto = backoffice_service.add_menus(data)
        if response.is_new:
            return DtoResponse.response(response, 201)
        return DtoResponse.response(response)
    except WeekendDateError as e:
        return ErrorResponse.response(e, 400)
    except PastDateModificationError as e:
        return ErrorResponse.response(e, 400)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /back/menus DELETE
@require_auth([UserRole.ADMIN, UserRole.MANAGER])
@deserialize
def delete_menu(request, data: DeleteMenuRequestDto) -> HttpResponse:
    try:
        response: CommonStatusResponseDto = backoffice_service.delete_menu(data)
        return DtoResponse.response(response)
    except PastDateModificationError as e:
        return ErrorResponse.response(e, 400)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /back/menus/excel? GET
@api_view(['GET'])
@require_auth([UserRole.ADMIN, UserRole.MANAGER])
@deserialize
def get_excel_file(request: HttpRequest, data: GetExcelFileRequestDto) -> HttpResponse:
    try:
        file_name = backoffice_service.get_excel_file(data)
        return FileResponse.response(file_path=file_name, content_type="application/vnd.ms-excel")
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /back/menus/history
@api_view(['GET'])
@require_auth([UserRole.ADMIN, UserRole.MANAGER])
@deserialize
def get_menu_modification_history(request, data: GetMenuHistoryRequestDto) -> HttpResponse:
    try:
        response = backoffice_service.get_menu_history(data=data)
        return DtoResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /back/users/role POST
@api_view(['POST'])
@require_auth([UserRole.ADMIN, UserRole.MANAGER])
@deserialize
def modify_user_role(request, data: ModifyUserRoleRequestDto, user: User) -> HttpResponse:
    try:
        response: CommonStatusResponseDto = backoffice_service.modify_user_role(data, user)
        return DtoResponse.response(response)
    except PermissionDeniedError as e:
        return ErrorResponse.response(e, 403)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


@api_view(['POST', 'DELETE'])
@multi_methods(POST=add_menu, DELETE=delete_menu)
def menu_methods_acceptor():
    pass
