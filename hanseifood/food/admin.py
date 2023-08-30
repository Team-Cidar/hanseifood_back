from django.contrib import admin
from food.models import Day, DayMeal, Meal

# Register your objs here.
admin.site.register(Day)
admin.site.register(DayMeal)
admin.site.register(Meal)