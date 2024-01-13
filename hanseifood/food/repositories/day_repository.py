from datetime import datetime

from typing import Tuple
from django.db.models import QuerySet

from ..models import Day
from ..repositories.abstract_repository import AbstractRepository


class DayRepository(AbstractRepository):
    def __init__(self):
        super(DayRepository, self).__init__(Day.objects)

    def findByDate(self, date: datetime) -> QuerySet:
        datas: QuerySet = self.manager.filter(date=date)
        return datas

    def existByDate(self, date: datetime) -> Tuple[bool, QuerySet]:
        datas: QuerySet = self.findByDate(date)
        return datas.exists(), datas

    # override
    def save(self, date: datetime) -> Day:
        entity = Day(date=date)
        entity.save()
        return entity
