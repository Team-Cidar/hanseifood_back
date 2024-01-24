from django.db.models import Model, Manager

from ..core.patterns.singleton_cls import Singleton


class AbstractRepository(metaclass=Singleton):
    def __init__(self, manager: Manager):
        self.manager: Manager = manager

    def clearAll(self):
        self.manager.all().delete()

    def update(self, model: Model) -> Model:
        return model.save()

    # abstract method
    def save(self, *args, **kwargs) -> Model:
        raise NotImplementedError("save(self, *args, **kwargs) method in child of AbstractRepository must be implemented.")
