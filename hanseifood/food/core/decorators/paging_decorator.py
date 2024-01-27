from django.http import QueryDict
from rest_framework.request import Request

from ..utils.decorator_utils import get_request_from_args
from ...dtos.general.paging_dto import PagingDto
from ...responses.error_response import ErrorResponse


def paging(view_method):
    def __get_raw_query_params(params: QueryDict) -> dict:
        query_params: dict = dict()
        for key, value in params.items():
            if len(value) == 1:
                query_params[key] = value[0]
            else:
                query_params[key] = value
        return query_params

    def __get_paging_obj(paging_data: dict) -> PagingDto:
        dto: PagingDto = PagingDto()
        page_no: int = int(paging_data.get('pageNo', 1))
        page_size: int = int(paging_data.get('pageSize', 10))
        setattr(dto, 'page_no', page_no)
        setattr(dto, 'page_size', page_size)
        return dto

    def pass_paging_obj(*args, **kwargs):
        try:
            request: Request = get_request_from_args(*args)
            paging_data: dict = __get_raw_query_params(request.query_params)

            kwargs['paging_data'] = __get_paging_obj(paging_data)
            return view_method(*args, **kwargs)
        except Exception as e:
            return ErrorResponse.response(e, 500)

    pass_paging_obj.__annotations__ = view_method.__annotations__
    return pass_paging_obj