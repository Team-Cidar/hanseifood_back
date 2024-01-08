import logging

from ..dtos.model_mapped.pay_info_dto import PayInfoDto
from ..dtos.model_mapped.ticket_dto import TicketDto
from ..dtos.model_mapped.user_dto import UserDto
from ..dtos.model_mapped.user_ticket_dto import UserTicketDto
from ..dtos.responses.ticket_response_dto import TicketValidationResponseDto
from .abstract_service import AbstractService

logger = logging.getLogger(__name__)


class TicketService(AbstractService):
    def __init__(self):
        # add repository instance variables
        pass

    def create_ticket(self) -> UserTicketDto:
        # qr만들 때 식권 id 암호화해서 qr 만들기
        pass

    def validate_ticket(self, ticket_id: str) -> TicketValidationResponseDto:
        # 식권 id 암호화 되어있으니 복호화 해서 id값 복원해서 사용
        # this is a temporary code
        # have to validate the ticket strictly, 사용 여부 등등도 다 체크해서 valid true로
        owner: UserDto = UserDto()
        ticket_info: TicketDto = TicketDto()
        ticket_info.ticket_id = ticket_id
        pay_info: PayInfoDto = PayInfoDto()
        ticket: UserTicketDto = UserTicketDto(owner=owner, ticket=ticket_info, pay_info=pay_info)

        ticket_validated: TicketValidationResponseDto = TicketValidationResponseDto(ticket=ticket)
        ticket_validated.is_valid = True
        ticket_validated.ticket.owner.nickname = 'Jeremy'
        ticket_validated.ticket.ticket.ticket_info = '학생 식당'
        return ticket_validated
