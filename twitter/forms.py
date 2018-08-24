from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.forms import ModelForm

from twitter.models import Tweet


class LoginForm(forms.Form):
    login = forms.CharField(widget=forms.EmailInput, label="E-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class RegisterForm(ModelForm):
    password_repeated = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput,
        label="Powtórz hasło",
        help_text=f"""Sugeruje się aby hasło miało cztery litery,
         zaczynało się na d i kończyło na a"""
    )

    class Meta:
        model = User
        fields = ("username", "password")
        labels = {"username": "Nazwa użytkownika",
                  "password": "Hasło",
                  }
        widgets = {"password": forms.PasswordInput}
        validators = {"username": EmailValidator}

    field_order = (
        "username",
        "password",
        "password_repeated",
    )


class AddBellRingForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        widgets = {
            'content': forms.Textarea(),
        }

