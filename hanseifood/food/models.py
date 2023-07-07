from django.db import models


# Create your models here.
class Day(models.Model):
    date = models.DateField(null=False)

    def __str__(self):
        return self.title


class Meal(models.Model):
    meal_name = models.TextField()

    def __str__(self):
        return self.title


class DayMeal(models.Model):
    day_id = models.ForeignKey(Day, on_delete=models.CASCADE)
    meal_id = models.ForeignKey(Meal, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title
