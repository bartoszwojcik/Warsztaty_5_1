from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView

from twitter.forms import AddBellRingForm, RegisterForm, LoginForm
from twitter.models import Tweet


# Main views

class HomeView(View):

    def get(self, request):
        return TemplateResponse(
            request,
            "base.html",
            {
                "bell_rings": Tweet.objects.all().order_by("-creation_date")
            }
        )


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["login"],
            password=form.cleaned_data["password"]
        )
        if user is not None:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(
                form=form,
                error="Wrong login data."
            ))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(
            form=form,
            error="Wrong login data."
        ))


def logout_view(request):
    logout(request)
    return redirect(reverse("home"))


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        if form.cleaned_data["password"] \
                == form.cleaned_data["password_repeated"]:
            User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["username"],
                email=form.cleaned_data["username"]
            )
            user_to_login = User.objects.get(
                username=form.cleaned_data["username"]
            )
            login(self.request, user_to_login)
            return redirect(reverse("home"))
        else:
            return self.render_to_response(self.get_context_data(
                form=form,
                pass_error="Hasło nie jest zgodne."
            ))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(
            form=form,
            error=form.errors
        ))


# Add a bell-ring (tweet)

class AddBellRingView(View):

    def get(self, request):
        form = AddBellRingForm()
        return render(request, 'ring_a_bell.html', {'form': form})

    def post(self, request):
        form = AddBellRingForm(request.POST)
        if form.is_valid():
            Tweet.objects.create(
                content=form.cleaned_data["content"],
                author=request.user
            )
            return redirect(reverse("home"))
        else:
            return render(
                request, 'ring_a_bell.html', {
                    'form': form
                }
            )
