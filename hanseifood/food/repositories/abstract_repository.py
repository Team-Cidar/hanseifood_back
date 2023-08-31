from abc import *


class AbstractRepository(metaclass=ABCMeta):
    def __init__(self, model):
        self.model = model
