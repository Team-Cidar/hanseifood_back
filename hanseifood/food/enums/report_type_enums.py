from enum import Enum


class ReportType(Enum):
    ILLEGAL = 1
    BAD_WORD = 2
    PRIVACY = 3
    SEXUAL = 4
    UNPLEASANT = 5
    SPAM = 6
    ETC = 0