from django.db.models import Model
from ..core.patterns.singleton_cls import Singleton


class AbstractRepository(metaclass=Singleton):
    def __init__(self, model):
        self.model = model

    def clearAll(self):
        self.model.all().delete()

    # abstract method
    def save(self, *args, **kwargs) -> Model:
        raise NotImplementedError("save(self, *args, **kwargs) method in child of AbstractRepository must be implemented.")
