from abc import *
from django.http import JsonResponse


class AbstractResponse(metaclass=ABCMeta):
    @abstractmethod
    def __serialize(self) -> dict:
        raise NotImplementedError

    def toJson(self):
        return JsonResponse(self.__serialize(), json_dumps_params={'ensure_ascii': False}, safe=False)
