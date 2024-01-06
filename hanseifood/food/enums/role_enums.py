from enum import Enum


class UserRole(Enum):
    A = 'admin'
    U = 'user'

    @classmethod
    def get_default_role(cls):
        return cls.U

    @classmethod
    def get_all(cls):
        return [cls.A, cls.U]

    @classmethod
    def from_name(cls, name: str):
        return cls[name]

    def __str__(self):
        return self.name