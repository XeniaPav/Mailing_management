import secrets

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)

from users.forms import UserRegisterForm, UserForm, UserProfileForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет! Перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserListView(LoginRequiredMixin, ListView, PermissionRequiredMixin):
    model = User
    template_name = "user_list.html"
    permission_required = "users.can_view_user"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = [
        "id",
        "email",
        "is_active",
    ]
    success_url = reverse_lazy("users:user_list")

    def get_form_class(self):
        user = self.request.user
        if user.has_perm("users.can_view_user") and user.has_perm(
            "users.can_block_user"
        ):
            return UserForm
        raise PermissionDenied


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users:user_list")


class NewPasswordView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = "users/new_password.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.get(email=email)
        if user:
            password = secrets.token_urlsafe(10)
            send_mail(
                subject="Новый пароль",
                message=f"Здравствуй! Новый пароль для входа в твой аккаунт: {password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            user.set_password(password)
            user.save()

            return redirect(reverse("users:login"))

        else:
            return redirect(reverse("users/new_password.html"))


class ProfileView(UpdateView):
    """Редактирование профиля пользователя"""

    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("blog:list")
    template_name = "users/profile.html"

    def get_object(self, queryset=None):
        """Переход на редактирование того, под кем сессия"""
        return self.request.user
