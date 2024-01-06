from .abstract_request_dto import RequestDto


class AddMenuRequestDto(RequestDto):
    datetime: str
    student: str
    employee: str
    additional: str