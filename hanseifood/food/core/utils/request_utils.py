from typing import List, Union

from ...exceptions.request_exceptions import MissingFieldError


def extract_request_datas(request_data: dict, fields: List[str]) -> Union[tuple, str, int]:
    try:
        if len(fields) == 1:
            return request_data[fields[0]]
        result: list = []
        for field in fields:
            result.append(request_data[field])
        return tuple(result)
    except KeyError:
        raise MissingFieldError(field_names=fields)
