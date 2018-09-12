from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView

from messaging.forms import AddBellRingForm, RegisterForm, LoginForm, \
    NewPMessageForm, NewCommentForm, ResetPasswordForm
from messaging.models import Tweet, PrivateMessage, Comment


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
                new_user = User.objects.create_user(
                    username=form.cleaned_data["email"].split("@")[0],
                    password=form.cleaned_data["password"],
                    email=form.cleaned_data["email"]
                )
            except IntegrityError:
                return self.render_to_response(self.get_context_data(
                    form=form,
                    error="User with that e-mail already exists."
                ))

            # Add permissions by adding user to a group
            new_user.groups.add(name="standard_users")

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


class ResetPasswordView(LoginRequiredMixin, FormView):
    template_name = 'reset_password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if str(request.user.pk) == self.kwargs["pk"]:
            return super(ResetPasswordView, self).dispatch(
                    request, *args, **kwargs
                )
        else:
            return HttpResponseForbidden('Forbidden.')

    def form_valid(self, form):
        if form.cleaned_data["password"] \
                == form.cleaned_data["password_repeated"]:
            user_data = User.objects.get(pk=self.kwargs["pk"])
            user_data.set_password(form.cleaned_data["password"])
            user_data.save()
            login(self.request, user_data)
            return redirect(reverse("home"))
        else:
            return self.render_to_response(self.get_context_data(
                form=form,
                pass_error="Passwords do not match."
            ))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(
            form=form,
            error=form.errors
        ))


# Add a bell-ring (tweet)

class AddBellRingView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "messaging.add_tweet"

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


class UserBellsView(LoginRequiredMixin, TemplateView):
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


class BellRingView(LoginRequiredMixin, FormView):
    template_name = "base/single_bell_ring.html"
    form_class = NewCommentForm
    success_url = ""

    def get_context_data(self, **kwargs):
        context = super(BellRingView, self).get_context_data(**kwargs)
        try:
            context["bell_ring"] = Tweet.objects.get(pk=self.kwargs["pk"])
        except:
            return Http404

        context["single"] = True

        return context

    def form_valid(self, form):
        Comment.objects.create(
            author=self.request.user,
            tweet=Tweet.objects.get(pk=self.kwargs["pk"]),
            content=form.cleaned_data["content"]
        )

        self.success_url = reverse_lazy(
            "bell-ring", kwargs={"pk": self.kwargs["pk"]}
        )

        return super(BellRingView, self).form_valid(form)


class UserPMessagesView(LoginRequiredMixin, ListView):
    template_name = "user-pmessages.html"
    model = PrivateMessage
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if str(request.user.pk) == self.kwargs["pk"]:
            return super(UserPMessagesView, self).dispatch(
                    request, *args, **kwargs
                )
        else:
            return HttpResponseForbidden('Forbidden.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['messages'] = PrivateMessage.objects.filter(
            Q(sender=self.kwargs["pk"])
            | Q(recipient=self.kwargs["pk"])
        ).distinct().order_by("-creation_date")

        return context


class SinglePMessageView(LoginRequiredMixin, DetailView):
    model = PrivateMessage
    opening_user = None
    this_message = None

    def dispatch(self, request, *args, **kwargs):
        self.this_message = PrivateMessage.objects.get(pk=self.kwargs["pk"])

        if self.this_message.recipient == request.user \
                or self.this_message.sender == request.user:
            self.opening_user = request.user
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('Forbidden.')

    def get_context_data(self, **kwargs):
        if self.opening_user == self.this_message.recipient:
            self.this_message.read_status = True
            self.this_message.save()

        self.this_message = None
        context = super().get_context_data(**kwargs)
        self.opening_user = None
        return context


class NewPMessageView(LoginRequiredMixin, FormView):
    template_name = 'new_pmessage.html'
    form_class = NewPMessageForm
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs["pk"] != str(request.user.id):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(
                'You cannot send a message to yourself.'
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipient"] = User.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        PrivateMessage.objects.create(
            sender=self.request.user,
            recipient=User.objects.get(pk=self.kwargs["pk"]),
            content=form.cleaned_data["content"],
            read_status=False
        )
        return super(NewPMessageView, self).form_valid(form)


# ToDo: User editing: information and password. Only theirs,
# ToDo: Only login and user creation accessible without login
# ToDo: Tasks 5, 6
