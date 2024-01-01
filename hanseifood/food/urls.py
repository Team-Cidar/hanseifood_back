from django.urls import path
from .views import base_views, menu_views, ticket_views, login_views, backoffice_views
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)
from .core.jwt import jwt


urlpatterns = [
    # /views/base_views
    path("", base_views.index, name="index"),

    # /views/menu_views
    path('menus/day', menu_views.get_todays_menu, name='daily_menu'),
    path('menus/week', menu_views.get_weekly_menus, name='weekly_menu'),
    path('menus/target', menu_views.get_target_days_menu, name='target_menu'),

    # /view/login_views
    path("login", login_views.try_login, name='try_login'),
    path("nickname", login_views.set_nickname, name="set_nickname"),
    path('api/token', jwt.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # /views/ticket_views
    path('tickets/validate/<str:ticket_id>', ticket_views.get_ticket_validation, name='validate_ticket'),

    # /views/backoffice_views
    path('back/menus', backoffice_views.add_menu, name='add_menu'),
    path('back/menus/excel', backoffice_views.get_excel_file, name='get_excel_file')
]
