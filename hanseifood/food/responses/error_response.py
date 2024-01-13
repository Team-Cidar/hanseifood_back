import logging
import traceback

from django.http import HttpResponse

from .abstract_response import AbstractResponse

logger = logging.getLogger(__name__)


class ErrorResponse(AbstractResponse):
    @staticmethod
    def response(data: BaseException, status_code: int = 500) -> HttpResponse:
        trace_back: str = traceback.format_exc()
        logger.error(trace_back)
        response = HttpResponse(str(data), status=status_code)

        return response
