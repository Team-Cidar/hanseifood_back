from django.db import models


# Create your models here.
class Day(models.Model):
    date = models.DateField(null=False)

    def __str__(self):
        return str(self.date)


class Meal(models.Model):
    meal_name = models.TextField()

    def __str__(self):
        return self.meal_name


class DayMeal(models.Model):
    day_id = models.ForeignKey(Day, on_delete=models.CASCADE)
    meal_id = models.ForeignKey(Meal, on_delete=models.DO_NOTHING)
    for_student = models.BooleanField()

    def __str__(self):
        return str(self.day_id) + '/' + str(self.meal_id)
