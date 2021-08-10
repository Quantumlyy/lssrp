from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from lssrp_app.forms import StyledUserCreationForm, StyledAuthenticationForm


class HomeView(TemplateView):
    template_name = "lssrp/base.html"


# https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m
def register_view(request):
    form = StyledUserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/")
    return render(request, "auth/register.html", {"form": form})


# https://stackoverflow.com/questions/31482178/django-login-page-for-non-admin-dashboard
def login_view(request):
    form = StyledAuthenticationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/")
    return render(request, "auth/login.html", {"form": form})
