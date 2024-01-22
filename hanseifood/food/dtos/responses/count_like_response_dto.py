from ..abstract_dto import Dto


class CountLikeResponseDto(Dto):
    def __init__(self, menu_id: str, like_count: int):
        self.menu_id: str = menu_id
        self.like_count: int = like_count