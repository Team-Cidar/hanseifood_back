from ..abstract_dto import Dto


class PagingDto(Dto):
    page_no: int
    page_size: int