from ..abstract_dto import Dto


class PayInfoDto(Dto):
    def __init__(self):
        self.pay_type: str = ''
        self.order_id: str = ''
        self.order_date: str = ''