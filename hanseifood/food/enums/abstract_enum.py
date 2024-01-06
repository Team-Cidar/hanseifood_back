from enum import Enum


class AbstractEnum(Enum):
    @classmethod
    def from_name(cls, name: str):
        return cls[name]

    def __str__(self):
        return self.name
