import datetime
from django.db.models import Model, QuerySet

from ..exceptions.menu_exceptions import EmptyDataError
from ..models import Day
from ..repositories.abstract_repository import AbstractRepository


class DayRepository(AbstractRepository):
    def __init__(self):
        super().__init__(Day.objects)

    def findByDate(self, date: datetime.datetime) -> QuerySet:
        datas: QuerySet = self.model.filter(date=date)
        # if not datas.exists():
        #     raise EmptyDataError(f"{date.strftime('%Y-%m-%d')} data is not exists")
        return datas

    # override
    def save(self, date: datetime.datetime) -> Model:
        entity = Day(date=date)
        entity.save()
        return entity
