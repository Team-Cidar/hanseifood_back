from ..abstract_dto import Dto


class MenuModificationResponseDto(Dto):
    def __init__(self, is_new: bool):
        self.is_new: bool = is_new