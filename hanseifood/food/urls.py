from django.urls import path
from . import views

urlpatterns = [
    path("student", views.student_food_table, name="student_food_table"),
    path("", views.index, name="student_food_table")
]
