from .abstract_model import AbstractModel
from ...core.constants.strings.exception_strings import MISSING_ARG_ERROR


# 기본적인 티켓 정보 리턴 dto
# 나중에 추가할 부분들 추가해야함
class TicketModel(AbstractModel):
    def __init__(self, ticket_id: str):
        self.ticket_id: str = ticket_id
        self.owner_name: str = ''

    # override
    def _serialize(self) -> dict:
        return {
            'ticket_id': self.ticket_id,
            'owner_name': self.owner_name,
        }


class TicketValidationModel(TicketModel):
    def __init__(self, ticket_id: str):
        super().__init__(ticket_id)
        self.is_valid: bool = False
        self.is_used: bool = False

    # override
    def _serialize(self) -> dict:
        res: dict = super()._serialize()
        res.update({
            'is_valid': self.is_valid,
            'is_used': self.is_used
        })
        return res
