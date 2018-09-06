from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from messaging.models import Tweet


class LoginForm(forms.Form):
    login = forms.CharField(widget=forms.EmailInput, label="E-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class RegisterForm(ModelForm):
    password_repeated = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput,
        label="Repeat password",
    )

    class Meta:
        model = User
        fields = ("email", "password")
        labels = {"email": "Your e-mail",
                  "password": "Password",
                  }
        widgets = {"password": forms.PasswordInput}

    field_order = (
        "email",
        "password",
        "password_repeated",
    )


class AddBellRingForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(),
        }


class NewPMessageForm(forms.ModelForm):
    pass


class NewCommentForm(forms.ModelForm):
    pass