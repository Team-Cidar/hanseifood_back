from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.type_exceptions import NotAbstractModelError
from ..responses.error_response import ErrorResponse
from ..responses.model_response import ModelResponse
from ..services.backoffice_service import BackOfficeService

backoffice_service: BackOfficeService = BackOfficeService()


# /back/menu POST
@api_view(['POST'])
@csrf_exempt
def add_menu(request: HttpRequest) -> HttpResponse:
    try:
        response = backoffice_service.add_menus()
        return ModelResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotAbstractModelError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)
