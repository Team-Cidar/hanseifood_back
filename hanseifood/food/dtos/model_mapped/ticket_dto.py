from ..abstract_dto import Dto


class TicketDto(Dto):
    def __init__(self):
        self.ticket_id: str = ''
        self.ticket_info: str = ''
        self.is_used: bool = False