from abc import *
from django.http import JsonResponse


class AbstractModel(metaclass=ABCMeta):
    @abstractmethod
    def _serialize(self) -> dict:
        raise NotImplementedError

    def toJson(self):
        return JsonResponse(self._serialize(), json_dumps_params={'ensure_ascii': False})

    @staticmethod
    def listToJson(datas):
        serialized_list = []
        data: AbstractModel
        for data in datas:
            serialized_list.append(data._serialize())
        return JsonResponse(serialized_list, json_dumps_params={'ensure_ascii': False}, safe=False)
