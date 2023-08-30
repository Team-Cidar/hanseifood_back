from django.http import HttpResponse

from ..exceptions.type_exceptions import NotAbstractModelError
from ..objs.abstract_model import AbstractModel
from ..objs.menu import MenuModel


class ModelResponse:
    @staticmethod
    def getResponse(data, status_code: int = 200) -> HttpResponse:
        if isinstance(data, AbstractModel):
            response = HttpResponse(data.toJson())
        elif isinstance(data, list) and all(isinstance(item, AbstractModel) for item in data):
            response = HttpResponse(MenuModel.listToJson(data))
        else:
            raise NotAbstractModelError()
        response.status_code = status_code

        return response
