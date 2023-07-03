from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_food_table, name="student_food_table")
]
