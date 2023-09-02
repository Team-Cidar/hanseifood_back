from abc import *
from django.db.models import Model


class AbstractRepository(metaclass=ABCMeta):
    def __init__(self, model):
        self.model = model

    def save(self, model_obj: Model):
        model_obj.save()