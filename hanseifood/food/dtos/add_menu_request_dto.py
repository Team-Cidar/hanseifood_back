from .abstract_dto import Dto


class AddMenuRequestDto(Dto):
    datetime: str
    student: str
    employee: str
    additional: str