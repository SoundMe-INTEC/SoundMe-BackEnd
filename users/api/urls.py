from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .user_view import UserView  

urlpatterns = [
    path("signup", UserView.signup, name="user-signup"),
    path("check", UserView.check, name="user-check"),
    path("login", UserView.login, name="user-login"),
    path("verify-otp", UserView.verify_otp, name="user-verify-otp"),
    path("profile", UserView.profile, name="user-profile"),
    path("reset-password", UserView.reset_password, name="user-reset-password"),
    path("users", UserView.search_users, name="user-search"),
    path("admin/users", UserView.list_admin, name="admin_list_users"),
    path("admin/users/create", UserView.admin_create_user, name="admin_create_user"),
    path("admin/users/update", UserView.update_user, name="admin_update_user"),
    path("admin/users/deactivate", UserView.deactivate_user, name="admin_deactivate_user"),
    path("admin/users/activate", UserView.activate_user, name="admin_activate_user"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
]