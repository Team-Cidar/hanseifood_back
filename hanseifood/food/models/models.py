import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import CustomUserManager


class Day(models.Model):
    date = models.DateField(unique_for_date=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        db_table = 'day'


class Meal(models.Model):
    meal_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.meal_name

    class Meta:
        db_table = 'meal'


class DayMeal(models.Model):
    day_id = models.ForeignKey(Day, on_delete=models.CASCADE)
    meal_id = models.ForeignKey(Meal, on_delete=models.DO_NOTHING)
    menu_type = models.CharField(max_length=1, default='N')  # N == None
    menu_id = models.CharField(max_length=40, null=False)

    # override
    def delete(self, using=None, keep_parents=False):
        deleted: DayMealDeleted = DayMealDeleted(
            day_id=self.day_id,
            meal_id=self.meal_id,
            menu_type=self.menu_type,
            menu_id=self.menu_id
        )
        deleted.save()
        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f"{str(self.day_id)} / {str(self.meal_id)} [{self.menu_type}]"

    class Meta:
        db_table = 'day_meal'


class DayMealDeleted(models.Model):
    day_id = models.ForeignKey(Day, on_delete=models.CASCADE)
    meal_id = models.ForeignKey(Meal, on_delete=models.DO_NOTHING)
    menu_type = models.CharField(max_length=1, default='N')
    menu_id = models.CharField(max_length=40, null=False)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.day_id}] - {self.deleted_at}"

    class Meta:
        db_table = 'day_meal_deleted'


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
        return f"[{self.kakao_name}/{self.nickname}/{self.role}] -> {self.email}"

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
    order_id = models.CharField(max_length=255, unique=True)
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


class MenuComment(models.Model):
    menu_id = models.CharField(max_length=40, null=False)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length=100)
    commented_at = models.DateTimeField(auto_now_add=True)

    # Override
    def delete(self, using=None, keep_parents=False):
        deleted: CommentDeleted = CommentDeleted(
            menu_id=self.menu_id,
            user_id=self.user_id,
            comment=self.comment,
            commented_at=self.commented_at
        )
        deleted.save()
        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f"[{self.user_id}] - {self.comment} ({self.menu_id})"

    class Meta:
        db_table = 'menu_comment'


class CommentReport(models.Model):
    menu_comment_id = models.ForeignKey(MenuComment, on_delete=models.DO_NOTHING)
    reporter = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    report_msg = models.CharField(max_length=30)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.reporter}] - {self.report_msg} / {self.menu_comment_id}"

    class Meta:
        db_table = 'comment_report'


class CommentDeleted(models.Model):
    menu_id =models.CharField(max_length=40, null=False)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length=100)
    commented_at = models.DateTimeField()
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.user_id}] - {self.comment} ({self.menu_id}) / {self.deleted_at}"

    class Meta:
        db_table = 'comment_deleted'


class MenuLike(models.Model):
    menu_id = models.CharField(max_length=40, null=False)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'[{self.user_id}] - {self.menu_id}'

    class Meta:
        db_table = 'menu_like'