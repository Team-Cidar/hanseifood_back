from datetime import datetime


class MissingFieldError(KeyError):
    def __init__(self, field_names, msg="Required arguments named {} are not provided."):
        super().__init__(msg.format(field_names))

class WeekendDateError(Exception):
    def __init__(self, date: datetime, msg="'{}' is weekend."):
        super(WeekendDateError, self).__init__(msg.format(date.strftime("%Y-%m-%d")))


class PastDateModificationError(Exception):
    def __init__(self, msg="Modification of past date's data is not allowed"):
        super(PastDateModificationError, self).__init__(msg)