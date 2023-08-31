from .abstract_repository import AbstractRepository
from ..exceptions.menu_exceptions import EmptyDataError
from ..models import DayMeal, Day


class DayMealRepository(AbstractRepository):
    def __init__(self):
        super().__init__(DayMeal.objects)

    def findByDayId(self, day_id: Day):
        datas = self.model.filter(day_id=day_id)
        if len(datas) == 0:
            raise EmptyDataError(f"{day_id.date}'s meal data is not exists")
        return datas