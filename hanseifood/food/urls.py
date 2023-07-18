from django.urls import path
from . import views

urlpatterns = [
    path("menus", views.get_menu, name="menu"),
    path("", views.index, name="index")
]
