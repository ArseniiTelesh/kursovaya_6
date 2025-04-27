from django.contrib.auth.forms import UserCreationForm
from django import forms

from mailing.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin,UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "password1": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Пароль"}
            ),
            "password2": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Повторите пароль"}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email