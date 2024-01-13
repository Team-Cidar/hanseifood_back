from abc import ABCMeta, abstractmethod

from typing import Any
from django.http import HttpResponse


class AbstractResponse(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def response(data: Any, status_code: int) -> HttpResponse:
        raise NotImplementedError
