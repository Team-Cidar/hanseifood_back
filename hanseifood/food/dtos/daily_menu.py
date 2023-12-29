from typing import List
from datetime import datetime


class DailyMenuDto:
    def __init__(self, date: datetime, student: list, employee: list, additional: list):
        self.date: datetime = date
        self.student: List[str] = student
        self.employee: List[str] = employee
        self.additional: List[str] = additional
