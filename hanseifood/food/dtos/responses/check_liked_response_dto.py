from ..abstract_dto import Dto


class CheckLikedResponseDto(Dto):
    def __init__(self, is_liked: bool):
        self.like: bool = is_liked