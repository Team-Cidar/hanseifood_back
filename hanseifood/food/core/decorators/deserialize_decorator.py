from typing import Type

from django.http import QueryDict
from rest_framework.request import Request

from ..utils.decorator_utils import get_request_from_args
from ...dtos.abstract_dto import Dto
from ...exceptions.type_exceptions import NotRequestDtoError
from ...responses.error_response import ErrorResponse


def deserialization(object_type: Type[Dto]):
    def decorator(view_method):
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

        def deserialize(*args, **kwargs):
            try:
                if not issubclass(object_type, Dto):
                    raise NotRequestDtoError(_type=object_type)

                request: Request = get_request_from_args(*args)
                data: dict = _get_req_data(request)

                deserialized_obj: Dto = object_type.deserialize(data)

                kwargs['data'] = deserialized_obj
                return view_method(*args, **kwargs)
            except Exception as e:
                return ErrorResponse.response(e, status_code=500)
        return deserialize
    return decorator