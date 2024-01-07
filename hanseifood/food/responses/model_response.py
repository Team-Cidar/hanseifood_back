from typing import Tuple, List, Union

from django.http import HttpResponse, JsonResponse

from .abstract_response import AbstractResponse
from ..dtos.abstract_dto import Dto
from ..exceptions.type_exceptions import NotAbstractModelError
from .objs.abstract_model import AbstractModel
from .objs.menu import MenuModel


class ModelResponse(AbstractResponse):
    @staticmethod
    def response(data: AbstractModel, status_code: int = 200) -> HttpResponse:
        if isinstance(data, AbstractModel):
            response = HttpResponse(data.toJson())
        elif isinstance(data, list) and all(isinstance(item, AbstractModel) for item in data):
            response = HttpResponse(MenuModel.listToJson(data))
        else:
            raise NotAbstractModelError(f"{type(data)} is not an instance of AbstractModel.")
        response.status_code = status_code

        return response


class DtoResponse:
    @staticmethod
    def response(data: Union[Dto, List[Dto], Tuple[Dto]], status_code: int = 200) -> HttpResponse:
        if isinstance(data, Dto):
            response_data = JsonResponse(data.serialize(), json_dumps_params={'ensure_ascii': False})
        elif isinstance(data, (list, tuple)) and all(isinstance(elem, Dto) for elem in data):
            response_data = JsonResponse(Dto.serialize_from_iter(data), json_dumps_params={'ensure_ascii': False}, safe=False)
        else:
            raise NotAbstractModelError(f"DtoResponse only allows for the data types of Dto or Iter[Dto]. But{type(data)} is not.")
        return HttpResponse(response_data, status=status_code)