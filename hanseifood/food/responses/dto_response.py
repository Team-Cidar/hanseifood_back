from typing import Tuple, List, Union
from django.http import HttpResponse, JsonResponse

from ..dtos.abstract_dto import Dto
from ..exceptions.type_exceptions import NotDtoClassError


class DtoResponse:
    @staticmethod
    def response(data: Union[Dto, List[Dto], Tuple[Dto]], status_code: int = 200) -> HttpResponse:
        if isinstance(data, Dto):
            response_data = JsonResponse(data.serialize(), json_dumps_params={'ensure_ascii': False})
        elif isinstance(data, (list, tuple)) and all(isinstance(elem, Dto) for elem in data):
            response_data = JsonResponse(Dto.serialize_from_iter(data), json_dumps_params={'ensure_ascii': False}, safe=False)
        else:
            raise NotDtoClassError(_type=type(data))
        return HttpResponse(response_data, status=status_code)