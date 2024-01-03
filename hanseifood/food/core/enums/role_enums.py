from enum import Enum


class UserRole(Enum):
    A = 'admin'
    U = 'user'

    @classmethod
    def from_name(cls, name: str):
        return cls[name]

    def __str__(self):
        return self.name
