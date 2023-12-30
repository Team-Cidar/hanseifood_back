from typing import List, Optional
from datetime import datetime

from django.db.models import Model


class DailyMenuDto:
    def __init__(self, date: Optional[datetime, Model], student: list, employee: list, additional: list):
        self.date: Optional[datetime, Model] = date
        self.student: List[str] = student
        self.employee: List[str] = employee
        self.additional: List[str] = additional
