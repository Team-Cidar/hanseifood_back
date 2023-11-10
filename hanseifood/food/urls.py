from django.urls import path
from .views import base_views, menu_views, ticket_views

urlpatterns = [
    # /views/base_views
    path("", base_views.index, name="index"),

    # /views/menu_views
    path('menus/day', menu_views.get_todays_menu, name='daily_menu'),
    path('menus/week', menu_views.get_weekly_menus, name='weekly_menu'),
    path('menus/target', menu_views.get_target_days_menu, name='target_menu'),

    # /views/ticket_views
    path('tickets/validate/<str:ticket_id>', ticket_views.get_ticket_validation, name='validate_ticket')
]
