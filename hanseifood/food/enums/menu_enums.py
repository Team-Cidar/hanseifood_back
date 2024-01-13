from enum import Enum


class MenuType(Enum):
    EMPLOYEE = 'E'
    STUDENT = 'S'
    ADDITIONAL = 'A'
    NONE = 'N'  # default type

    @classmethod
    def from_value(cls, value: str):
        return cls(value)

    @classmethod
    def get_all_except_default(cls):
        return [cls.EMPLOYEE, cls.STUDENT, cls.ADDITIONAL]

    def __str__(self):
        return self.value