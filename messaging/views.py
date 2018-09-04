from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, FormView

from messaging.forms import AddBellRingForm, RegisterForm, LoginForm
from messaging.models import Tweet


# Main views

class HomeView(View):

    def get(self, request):
        return TemplateResponse(
            request,
            "base.html",
            {
                "bell_rings": Tweet.objects.all().order_by("-creation_date"),
            }
        )


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["login"].split("@")[0],
            email=form.cleaned_data["login"],
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

            try:
                User.objects.create_user(
                    username=form.cleaned_data["email"].split("@")[0],
                    password=form.cleaned_data["password"],
                    email=form.cleaned_data["email"]
                )
            except IntegrityError:
                return self.render_to_response(self.get_context_data(
                    form=form,
                    error="User with that e-mail already exists."
                ))

            user_to_login = User.objects.get(
                username=form.cleaned_data["email"].split("@")[0]
            )
            login(self.request, user_to_login)
            return redirect(reverse("home"))

        else:
            return self.render_to_response(self.get_context_data(
                form=form,
                error="Passwords do not match."
            ))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(
            form=form,
            error=form.errors
        ))


# Add a bell-ring (tweet)

class AddBellRingView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "add_tweet"

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


class UserBellsView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, *args, **kwargs):
        try:
            author_data = User.objects.get(pk=kwargs["pk"])
        except:
            return Http404

        context = super(UserBellsView, self).get_context_data(*args, **kwargs)
        context["bell_rings"] = Tweet.objects.filter(
            author=author_data
        ).order_by(
            "-creation_date"
        )
        context["title"] = author_data.username + "'s Bell-Rings"
        return context


class BellRingView(TemplateView):
    template_name = "base/single_bell_ring.html"

    def get_context_data(self, *args, **kwargs):
        try:
            bell_ring_data = Tweet.objects.get(pk=kwargs["pk"])
        except:
            return Http404

        context = super(BellRingView, self).get_context_data(*args, **kwargs)
        context["bell_ring"] = bell_ring_data
        return context
