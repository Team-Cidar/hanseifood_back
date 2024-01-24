from ..abstract_dto import Dto


class CommonStatusResponseDto(Dto):
    def __init__(self, status: bool=True, msg: str='succeed'):
        self.status: bool = status
        self.msg: str = msg if status else 'failed'