from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from lssrp_app.forms import StyledUserCreationForm, StyledAuthenticationForm
from lssrp_app.utils import auth


class HomeView(TemplateView):
    template_name = "lssrp/base.html"


# https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m
def register_view(request):
    register_form = StyledUserCreationForm(request.POST)
    if register_form.is_valid():
        register_form.save()
        username = register_form.cleaned_data.get("username")
        password = register_form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(auth.next(request))
    return render(request, "auth/register.html", {"form": register_form})


# https://stackoverflow.com/questions/31482178/django-login-page-for-non-admin-dashboard
def login_view(request):
    login_form = StyledAuthenticationForm(request=request, data=request.POST)
    if login_form.is_valid():
        login_form.clean()
        login(request, login_form.get_user())
        return redirect(auth.next(request))
    return render(request, "auth/login.html", {"form": login_form})
