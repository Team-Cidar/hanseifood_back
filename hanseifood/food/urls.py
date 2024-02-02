from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import base_views, menu_views, ticket_views, login_views, backoffice_views, comment_views, like_views

urlpatterns = [
    # /views/base_views
    path("", base_views.index, name="index"),

    # /views/menu_views
    path('menus/day', menu_views.get_today_menu, name='daily_menu'),
    path('menus/week', menu_views.get_weekly_menus, name='weekly_menu'),
    path('menus/target', menu_views.get_target_days_menu, name='target_menu'),
    path('menus/<str:menu_id>', menu_views.get_menus_by_id, name='menu_by_id'),

    # /view/login_views
    path("login", login_views.try_login, name='try_login'),
    path("signup", login_views.create_user, name="create_user"),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),

    # /views/ticket_views
    path('tickets/validate/<str:ticket_id>', ticket_views.get_ticket_validation, name='validate_ticket'),

    # /views/backoffice_views
    path('back/menus', backoffice_views.menu_methods_acceptor, name='add_delete_menu'),  # POST DELETE
    path('back/menus/excel', backoffice_views.get_excel_file, name='get_excel_file'),
    path('back/menus/history', backoffice_views.get_menu_modification_history, name='get_menu_modification_history'),
    path('back/users/role', backoffice_views.modify_user_role, name='modify_user_role'),

    # /views/comment_views
    path('comments/menus', comment_views.comments_multi_methods_acceptor, name='add_delete_get_comments'),  # GET POST DELETE
    path('comments/menus/users', comment_views.get_comment_by_user, name='get_comments_by_user'),
    path('comments/report', comment_views.comments_report_methods_acceptor, name='report_get_reported_comments'),  # GET POST

    # /views/like_views
    path('likes/menus', like_views.like_multi_methods_acceptor, name='toggle_check_liked_menus'),  # GET POST
    path('likes/menus/count', like_views.count_likes_by_menu_id, name='count_liked_menus'),
    path('likes/menus/users', like_views.get_liked_menus_by_user, name='liked_menus_by_user')
]
