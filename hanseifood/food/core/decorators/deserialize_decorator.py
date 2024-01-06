from typing import Type, Tuple
from django.http import QueryDict
from rest_framework.request import Request

from ..utils.decorator_utils import get_request_from_args
from ...dtos.abstract_request_dto import RequestDto
from ...responses.error_response import ErrorResponse


def deserialize(view_method):
    def _get_raw_query_params(params: QueryDict) -> dict:
        query_params: dict = dict()
        for key, value in params.items():
            if len(value) == 1:
                query_params[key] = value[0]
            else:
                query_params[key] = value
        return query_params

    def _get_req_data(request: Request) -> dict:
        data: dict = request.data
        data.update(_get_raw_query_params(request.query_params))
        return data

    def _get_target_datatype_pair() -> Tuple[str, Type[RequestDto]]:
        for arg in view_method.__annotations__.items():
            if issubclass(arg[1], RequestDto):
                return arg

    def pass_deserialized_obj(*args, **kwargs):
        try:
            key, _type = _get_target_datatype_pair()

            request: Request = get_request_from_args(*args)
            data: dict = _get_req_data(request)

            deserialized_obj: RequestDto = _type.deserialize(data)

            kwargs[key] = deserialized_obj
            return view_method(*args, **kwargs)
        except Exception as e:
            return ErrorResponse.response(e, status_code=500)
    return pass_deserialized_obj