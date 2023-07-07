from django.db import models


# Create your models here.
class Days(models.Model):
    date = models.DateField(null=False)

    def __str__(self):
        return self.title