from typing import List

from ...models import Day


class DailyMenuDto:
    def __init__(self, date: Day, student: list, employee: list, additional: list):
        self.date: Day = date
        self.student: List[str] = student
        self.employee: List[str] = employee
        self.additional: List[str] = additional
