from django.db.models import Model, Manager, QuerySet

from ..core.patterns.singleton_cls import Singleton


class AbstractRepository(metaclass=Singleton):
    def __init__(self, manager: Manager):
        self.manager: Manager = manager

    def clearAll(self):
        self.delete_models(self.manager.all())

    def all(self):
        return self.manager.all()

    def update(self, model: Model) -> Model:
        result = model.save()
        return result

    def delete(self, model: Model):
        model.delete()

    def delete_models(self, models: QuerySet):
        model: Model
        for model in models:
            model.delete()

    # abstract method
    def save(self, *args, **kwargs) -> Model:
        raise NotImplementedError("save(self, *args, **kwargs) method in child of AbstractRepository must be implemented.")
