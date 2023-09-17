from django.http import HttpResponse

from .abstract_response import AbstractResponse


class ErrorResponse(AbstractResponse):
    @staticmethod
    def response(data: BaseException, status_code: int = 500) -> HttpResponse:
        response = HttpResponse(str(data))
        response.status_code = status_code

        return response
