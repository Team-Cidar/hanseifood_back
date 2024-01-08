from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import base_views, menu_views, ticket_views, login_views, backoffice_views


urlpatterns = [
    # /views/base_views
    path("", base_views.index, name="index"),

    # /views/menu_views
    path('menus/day', menu_views.get_today_menu, name='daily_menu'),
    path('menus/week', menu_views.get_weekly_menus, name='weekly_menu'),
    path('menus/target', menu_views.get_target_days_menu, name='target_menu'),

    # /view/login_views
    path("login", login_views.try_login, name='try_login'),
    path("signup", login_views.create_user, name="create_user"),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),

    # /views/ticket_views
    path('tickets/validate/<str:ticket_id>', ticket_views.get_ticket_validation, name='validate_ticket'),

    # /views/backoffice_views
    path('back/menus', backoffice_views.add_menu, name='add_menu'),
    path('back/menus/excel', backoffice_views.get_excel_file, name='get_excel_file')
]
