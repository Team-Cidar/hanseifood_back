from enum import Enum


class UserRole(Enum):
    ADMIN = 'A'
    MANAGER = 'M'
    USER = 'U'

    @classmethod
    def get_default_role(cls):
        return cls.USER

    @classmethod
    def get_all(cls):
        return [cls.ADMIN, cls.MANAGER, cls.USER]

    @classmethod
    def from_value(cls, value: str):
        return cls(value)

    def __str__(self):
        return self.value