from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import CustomUserManager


class Day(models.Model):
    date = models.DateField(null=False)

    def __str__(self):
        return str(self.date)

    class Meta:
        db_table = 'day'


class Meal(models.Model):
    meal_name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.meal_name

    class Meta:
        db_table = 'meal'


class DayMeal(models.Model):
    day_id = models.ForeignKey(Day, on_delete=models.CASCADE)
    meal_id = models.ForeignKey(Meal, on_delete=models.DO_NOTHING)
    for_student = models.BooleanField()
    is_additional = models.BooleanField(default=False)

    def __str__(self):
        return str(self.day_id) + '/' + str(self.meal_id)

    class Meta:
        db_table = 'day_meal'


class User(AbstractBaseUser):
    # PROVIDED FIELD : password, is_active, last_login
    kakao_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(null=True)
    kakao_name = models.TextField()
    nickname = models.TextField()
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=1)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.kakao_name}/{self.nickname}] -> {self.email}"

    class Meta:
        db_table = 'user'

    objects = CustomUserManager()  # ManagerClass()
    USERNAME_FIELD = 'kakao_id'
    REQUIRED_FIELDS = ['nickname']


class Ticket(models.Model):
    ticket_info = models.TextField()
    is_used = models.BooleanField()
    used_at = models.DateTimeField()
    create_at = models.DateTimeField()

    def __str__(self):
        return f"[{self.ticket_info}] -> used: {self.is_used}{f', used_at: {self.used_at}' if self.is_used else ''}"

    class Meta:
        db_table = 'ticket'


class PayInfo(models.Model):
    pay_type = models.TextField()
    order_id = models.TextField()
    order_date = models.DateTimeField()
    create_at = models.DateTimeField()

    def __str__(self):
        return f"[{self.pay_type} / {self.order_id}] -> order_date: {self.order_date}"

    class Meta:
        db_table = 'pay_info'


class UserTicket(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ticket_id = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    pay_id = models.ForeignKey(PayInfo, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"[{self.user_id} / {self.ticket_id} / {self.pay_id}]"

    class Meta:
        db_table = 'user_ticket'
