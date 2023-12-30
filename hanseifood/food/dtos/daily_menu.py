from typing import List, Union
from datetime import datetime

from django.db.models import Model


class DailyMenuDto:
    def __init__(self, date: Union[datetime, Model], student: list, employee: list, additional: list):
        self.date: Union[datetime, Model] = date
        self.student: List[str] = student
        self.employee: List[str] = employee
        self.additional: List[str] = additional
