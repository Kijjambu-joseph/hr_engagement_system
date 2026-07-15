
from django.urls import path
from . import views
from django.urls import path
from .views import (
    LoginAPIView,
    LogoutAPIView,
    CurrentUserAPIView,
    UpdateProfileAPIView,
    ChangePasswordAPIView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
    RefreshTokenAPIView,
)

urlpatterns = [
    path("login", views.login_page, name="login-page"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("me/", CurrentUserAPIView.as_view(), name="current-user"),
    path("profile/", UpdateProfileAPIView.as_view(), name="profile-update"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("token/refresh/", RefreshTokenAPIView.as_view(), name="token-refresh"),
    path('', views.home, name='home'),]
