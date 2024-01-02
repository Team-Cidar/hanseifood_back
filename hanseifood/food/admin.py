from django.contrib import admin
from .models import Day, DayMeal, Meal, User

# Register your objs here.
admin.site.register(Day)
admin.site.register(DayMeal)
admin.site.register(Meal)
admin.site.register(User)