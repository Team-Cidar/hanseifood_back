import datetime
from django.db.models import Model, QuerySet

from ..models import Day
from ..repositories.abstract_repository import AbstractRepository


class DayRepository(AbstractRepository):
    def __init__(self):
        super(DayRepository, self).__init__(Day.objects)

    def findByDate(self, date: datetime.datetime) -> QuerySet:
        datas: QuerySet = self.model.filter(date=date)
        return datas

    # override
    def save(self, date: datetime.datetime) -> Model:
        entity = Day(date=date)
        entity.save()
        return entity
