from django.http import HttpResponse

from ..exceptions.menu_exceptions import EmptyDataError
from ..exceptions.type_exceptions import NotAbstractModelError

import logging
logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response: HttpResponse
        try:
            response = self.get_response(request)
        except EmptyDataError as e:
            response = HttpResponse("Resource Not Found")
            response.status_code = 404
            logging.error(e)
        except NotAbstractModelError as e:
            response = HttpResponse("Server Response Error")
            response.status_code = 500
            logging.error(e)
        except Exception as e:
            response = HttpResponse("Unknown Server Error")
            response.status_code = 500
            logging.error(e)

        return response
