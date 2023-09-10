from django.urls import path
from . import views

urlpatterns = [
    path("menus/day", views.get_todays_menu, name="daily_menu"),
    path('menus/week', views.get_weekly_menus, name='weekly_menu'),
    path('menus/target', views.get_target_days_menu, name='target_menu'),
    path("", views.index, name="index")
]
