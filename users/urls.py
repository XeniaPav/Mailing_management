from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    UserCreateView,
    email_verification,
    UserUpdateView,
    UserDeleteView,
    UserListView,
    UserDetailView,
    NewPasswordView,
    ProfileView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>", email_verification, name="email-confirm"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("users/<int:pk>/update", UserUpdateView.as_view(), name="user_update"),
    path("users/<int:pk>/delete", UserDeleteView.as_view(), name="user_delete"),
    path("new_password/", NewPasswordView.as_view(), name="new_password"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
