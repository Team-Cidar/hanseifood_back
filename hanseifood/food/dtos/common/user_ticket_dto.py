from .pay_info_dto import PayInfoDto
from .ticket_dto import TicketDto
from .user_dto import UserDto
from ..abstract_dto import Dto


class UserTicketDto(Dto):
    def __init__(self, owner: UserDto, ticket: TicketDto, pay_info: PayInfoDto):
        self.owner: UserDto = owner
        self.ticket: TicketDto = ticket
        self.pay_info: PayInfoDto = pay_info