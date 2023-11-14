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
    is_additional = models.BooleanField(default=False)

    def to_dto(self):
        return DayMealDto(
            date=self.day_id.date,
            meal_name=self.meal_id.meal_name,
            for_student=self.for_student,
            is_additional=self.is_additional
        )

    def __str__(self):
        return str(self.day_id) + '/' + str(self.meal_id)


class User(models.Model):
    email = models.TextField()
    password = models.TextField()
    name = models.TextField()
    nickname = models.TextField()
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()

    def to_dto(self):
        pass

    def __str__(self):
        return f"[{self.name}/{self.nickname}] -> {self.email}"


class Ticket(models.Model):
    ticket_info = models.TextField()
    is_used = models.BooleanField()
    used_at = models.DateTimeField()
    create_at = models.DateTimeField()

    def to_dto(self):
        pass

    def __str__(self):
        return f"[{self.ticket_info}] -> used: {self.is_used}{f', used_at: {self.used_at}' if self.is_used else ''}"


class PayInfo(models.Model):
    pay_type = models.TextField()
    order_id = models.TextField()
    order_date = models.DateTimeField()
    create_at = models.DateTimeField()

    def to_dto(self):
        pass

    def __str__(self):
        return f"[{self.pay_type} / {self.order_id}] -> order_date: {self.order_date}"


class UserTicket(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ticket_id = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    pay_id = models.ForeignKey(PayInfo, on_delete=models.DO_NOTHING)

    def to_dto(self):
        pass

    def __str__(self):
        return f"[{self.user_id} / {self.ticket_id} / {self.pay_id}]"
