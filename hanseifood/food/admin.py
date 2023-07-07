from django.contrib import admin
from .models import Day, DayMeal, Meal

# Register your models here.
admin.site.register(Day)
admin.site.register(DayMeal)
admin.site.register(Meal)