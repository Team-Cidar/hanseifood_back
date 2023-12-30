from typing import List, Union
from datetime import datetime
from ..models import Day


class DailyMenuDto:
    def __init__(self, date: Union[datetime, Day], student: list, employee: list, additional: list):
        self.date: Union[datetime, Day] = date
        self.student: List[str] = student
        self.employee: List[str] = employee
        self.additional: List[str] = additional
