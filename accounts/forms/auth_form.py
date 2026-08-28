from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class CreateUserForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "Digite seu email",
            }
        ),
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "placeholder": "Digite seu username",
            }
        ),
    )
    password = forms.CharField(
        max_length=24,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Digite sua senha",
            }
        ),
    )
    password_confirmation = forms.CharField(
        max_length=24,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "Repita sua senha"}
        ),
    )

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise ValidationError("Usuario com email já registrado!")

        return self.cleaned_data["email"]

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data["username"]).exists():
            raise ValidationError("Usuario com username já registrado!")

        return self.cleaned_data["username"]

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)

        return password

    def clean(self):
        data = super().clean()

        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if password != password_confirmation:
            raise ValidationError("Senhas não coincidem")

        return data


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "placeholder": "Digite seu username",
            }
        ),
    )

    password = forms.CharField(
        max_length=24,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Digite sua senha",
            }
        ),
    )
