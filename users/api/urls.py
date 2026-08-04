from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from user_view import UserView  

urlpatterns = [
    path("signup/", UserView.signup, name="user-signup"),
    path("login/", UserView.login, name="user-login"),
    path("profile/", UserView.profile, name="user-profile"),
    path("reset-password/", UserView.reset_password, name="user-reset-password"),
    path("users/", UserView.search_users, name="user-search"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]