from enum import Enum


class UserRole(Enum):
    A = 'admin'
    U = 'user'


    @classmethod
    def from_name(cls, name: str):
        return cls[name]

    @classmethod
    def get_default_role(cls):
        return cls.U

    @classmethod
    def get_all(cls):
        return [cls.A, cls.U]

    def __str__(self):
        return self.name
