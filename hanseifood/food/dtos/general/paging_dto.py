from typing import List

from django.core.paginator import Paginator, Page

from ..abstract_dto import Dto


class PagingDto(Dto):
    page_no: int
    page_size: int


class PagingResponseDto(Dto):
    def __init__(self, page: Page, data: List[Dto]):
        paginator: Paginator = page.paginator
        self.page_size: int = paginator.per_page
        self.page_no: int = page.number
        self.max_page: int = paginator.num_pages
        self.datas: List[Dto] = data
