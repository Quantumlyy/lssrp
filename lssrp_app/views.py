from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = "lssrp/base.html"


# https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m
def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/")
    return render(request, "lssrp/register.html", {"form": form})