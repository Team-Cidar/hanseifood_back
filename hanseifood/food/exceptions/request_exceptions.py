from datetime import datetime


class MissingFieldError(KeyError):
    def __init__(self, field_names, msg="Required arguments named {} are not provided."):
        super().__init__(msg.format(field_names))

class WeekendDateError(Exception):
    def __init__(self, date: datetime, msg="'{}' is weekend."):
        super().__init__(msg.format(date.strftime("%Y-%m-%d")))