from abc import *
from django.db.models import Model


class AbstractRepository(metaclass=ABCMeta):
    def __init__(self, model):
        self.model = model

    def clearAll(self):
        self.model.all().delete()

    @abstractmethod
    def save(self, *args, **kwargs) -> Model:
        raise NotImplementedError("save(self, *args, **kwargs) method in child of AbstractRepository must be implemented.")
