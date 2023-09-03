from django.db import models
from .dtos.day import DayDto
from .dtos.meal import MealDto
from .dtos.day_meal import DayMealDto


# Create your models here.
class Day(models.Model):
    date = models.DateField(null=False)

    def to_dto(self):
        return DayDto(self.date)

    def __str__(self):
        return str(self.date)


class Meal(models.Model):
    meal_name = models.TextField()

    def to_dto(self):
        return MealDto(self.meal_name)

    def __str__(self):
        return self.meal_name


class DayMeal(models.Model):
    day_id = models.ForeignKey(Day, on_delete=models.CASCADE)
    meal_id = models.ForeignKey(Meal, on_delete=models.DO_NOTHING)
    for_student = models.BooleanField()
    is_additional = models.BooleanField()

    def to_dto(self):
        return DayMealDto(
            date=self.day_id.date,
            meal_name=self.meal_id.meal_name,
            for_student=self.for_student,
            is_additional=self.is_additional
        )

    def __str__(self):
        return str(self.day_id) + '/' + str(self.meal_id)
