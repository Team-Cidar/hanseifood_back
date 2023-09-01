import datetime

from typing import List

from ..exceptions.menu_exceptions import EmptyDataError
from ..models import Day
from ..repositories.abstract_repository import AbstractRepository


class DayRepository(AbstractRepository):
    def __init__(self):
        super().__init__(Day.objects)

    def findByDate(self, date: datetime.date) -> List[Day]:
        datas = self.model.filter(date=date)
        if len(datas) == 0:
            raise EmptyDataError(f"{date.strftime('%Y-%m-%d')} data is not exists")
        return datas
