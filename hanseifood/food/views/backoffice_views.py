from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from ..core.constants.strings.exception_strings import MISSING_REQUEST_FIELD_ERROR
from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.request_exceptions import MissingFieldError
from ..exceptions.type_exceptions import NotAbstractModelError
from ..responses.error_response import ErrorResponse
from ..responses.model_response import ModelResponse
from ..responses.objs.menu_modification import MenuModificationModel
from ..services.backoffice_service import BackOfficeService

backoffice_service: BackOfficeService = BackOfficeService()


# /back/menu POST
@api_view(['POST'])
@csrf_exempt
def add_menu(request: HttpRequest) -> HttpResponse:
    try:
        data: dict = request.data
        response: MenuModificationModel = backoffice_service.add_menus(data)
        if response.is_created:
            return ModelResponse.response(response, status_code=201)
        else:
            return ModelResponse.response(response)
    except KeyError:
        return ErrorResponse.response(MissingFieldError(MISSING_REQUEST_FIELD_ERROR.field_name(['datetime',
                                                                                                'student',
                                                                                                'employee',
                                                                                                'additional'])), status_code=400)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)


# /back/excel GET
@api_view(['GET'])
def get_excel_file(request: HttpRequest) -> HttpResponse:
    try:
        response = backoffice_service.get_excel_file()
        return HttpResponse("file", status=200)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)