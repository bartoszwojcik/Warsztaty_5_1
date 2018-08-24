"""workshop_5_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from twitter.views import HomeView, AddBellRingView, LoginView, logout_view,\
    RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^$", HomeView.as_view(), name="home"),
    re_path(r"^ring-a-bell/$", AddBellRingView.as_view(), name="ring-a-bell"),
    re_path(r"^login/$", LoginView.as_view(), name="login"),
    re_path(r"^logout/$", logout_view, name="logout"),
    re_path(r"^register/$", RegisterView.as_view(), name="register"),
]
