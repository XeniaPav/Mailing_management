from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django import forms
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("is_active",)


class UserProfileForm(UserChangeForm):
    """Форма редактирования профиля пользователя"""

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "avatar")

    def __init__(self, *args, **kwargs):
        """скрытие пароля при редактировании"""
        super().__init__(*args, **kwargs)

        self.fields["password"].widget = forms.HiddenInput()
