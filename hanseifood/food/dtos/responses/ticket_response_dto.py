from ..abstract_dto import Dto
from ..model_mapped.user_ticket_dto import UserTicketDto


class TicketValidationResponseDto(Dto):
    def __init__(self, ticket: UserTicketDto):
        self.is_valid: bool = False
        self.ticket: UserTicketDto = ticket
