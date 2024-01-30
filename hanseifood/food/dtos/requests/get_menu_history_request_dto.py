from ..abstract_dto import Dto
from ...enums.menu_enums import MenuType


class GetMenuHistoryRequestDto(Dto):
    date: str
    menu_type: MenuType