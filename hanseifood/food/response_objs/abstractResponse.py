from abc import *
from django.http import JsonResponse


class AbstractResponse(metaclass=ABCMeta):
    @abstractmethod
    def __serialize(self) -> dict:
        raise NotImplementedError

    def toJson(self):
        return JsonResponse(self.__serialize(), json_dumps_params={'ensure_ascii': False})

    @staticmethod
    def listToJson(datas):
        serialized_list = []
        for data in datas:
            serialized_list.append(data.__serialize())
        return JsonResponse(serialized_list, json_dumps_params={'ensure_ascii': False}, safe=False)