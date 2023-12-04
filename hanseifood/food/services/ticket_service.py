import logging

from ..responses.objs.ticket import TicketModel, TicketValidationModel
from .abstract_service import AbstractService

logger = logging.getLogger(__name__)


class TicketService(AbstractService):
    def __init__(self):
        # add repository instance variables
        pass

    def create_ticket(self) -> TicketModel:
        # qr만들 때 식권 id 암호화해서 qr 만들기
        pass

    def validate_ticket(self, ticket_id: str) -> TicketModel:
        # 식권 id 암호화 되어있으니 복호화 해서 id값 복원해서 사용
        # this is a temporary code
        # have to validate the ticket strictly, 사용 여부 등등도 다 체크해서 valid true로
        ticket_model: TicketValidationModel = TicketValidationModel(ticket_id)
        ticket_model.is_valid = True
        ticket_model.owner_name = 'Jeremy'
        ticket_model.ticket_type = '추가 메뉴'
        print(ticket_model)
        return ticket_model
