from ..abstract_dto import Dto


class CommonStatusResponseDto(Dto):
    def __init__(self, status: bool):
        self.status: bool = status