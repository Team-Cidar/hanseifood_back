from django.db.models import Model
from django.db.models.manager import BaseManager

from ..core.patterns.singleton_cls import Singleton


class AbstractRepository(metaclass=Singleton):
    def __init__(self, manager: BaseManager):
        self.manager: BaseManager = manager

    def clearAll(self):
        self.manager.all().delete()

    def delete(self, target_model: Model):
        target_model.delete()

    # abstract method
    def save(self, *args, **kwargs) -> Model:
        raise NotImplementedError("save(self, *args, **kwargs) method in child of AbstractRepository must be implemented.")
