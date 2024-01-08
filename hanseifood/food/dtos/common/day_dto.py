from ..abstract_dto import Dto
from ...models import Day


class DayDto(Dto):
    def __init__(self):
        self.date: str = ''

    @classmethod
    def from_model(cls, day_model: Day):
        day: DayDto = cls()
        day.date = day_model.date.strftime('%Y-%m-%d')
        return day