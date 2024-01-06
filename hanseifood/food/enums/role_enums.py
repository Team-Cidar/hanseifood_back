from .abstract_enum import AbstractEnum


class UserRole(AbstractEnum):
    A = 'admin'
    U = 'user'

    @classmethod
    def get_default_role(cls):
        return cls.U

    @classmethod
    def get_all(cls):
        return [cls.A, cls.U]
