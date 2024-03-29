from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view

from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.type_exceptions import NotDtoClassError
from ..responses.error_response import ErrorResponse
from ..responses.dto_response import DtoResponse
from ..services.ticket_service import TicketService

ticket_service = TicketService()


# /tickets/validate/<str:ticket_id> GET
@api_view(['GET'])
def get_ticket_validation(request: HttpRequest, ticket_id: str) -> HttpResponse:
    try:
        response = ticket_service.validate_ticket(ticket_id)
        return DtoResponse.response(response)
    except EmptyDataError as e:
        return ErrorResponse.response(e, 404)
    except NotDtoClassError as e:
        return ErrorResponse.response(e, 500)
    except ValueError as e:
        return ErrorResponse.response(e, 500)
    except Exception as e:
        return ErrorResponse.response(e, 500)
