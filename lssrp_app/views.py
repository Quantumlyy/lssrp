from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from lssrp_core import settings
from lssrp_app import models
from lssrp_app.forms import (
    StyledUserCreationForm,
    StyledAuthenticationForm,
)
from lssrp_app.utils import auth


@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class HomeView(TemplateView):
    template_name = "lssrp/base.html"


@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class MailView(TemplateView):
    template_name = "lssrp/mail/home.html"
    model = models.MailProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profile"] = models.MailProfile.objects.get(user=self.request.user)
        context["target"] = models.Email.objects.filter(receiver=context["profile"])

        return context


@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class MailSentView(TemplateView):
    template_name = "lssrp/mail/home.html"
    model = models.MailProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profile"] = models.MailProfile.objects.get(user=self.request.user)
        context["target"] = models.Email.objects.filter(sender=context["profile"])

        return context


@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class EmailView(TemplateView):
    template_name = "lssrp/mail/email.html"
    model = models.Email

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profile"] = models.MailProfile.objects.get(user=self.request.user)
        context["email"] = models.Email.objects.get(
            Q(id=kwargs["pk"]),
            Q(receiver=context["profile"]) | Q(sender=context["profile"]),
        )

        return context


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class MailComposeView(CreateView):
    template_name = "lssrp/mail/compose.html"
    model = models.Email
    fields = ["receiver", "title", "content"]
    success_url = "/mail"

    def form_valid(self, form):
        form.instance.sender = self.request.user.mail

        return super().form_valid(form)


@method_decorator(xframe_options_exempt, name="dispatch")
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL + "?next=/mail/")


@method_decorator(xframe_options_exempt, name="dispatch")
class CloseView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL + "?next=/mail/")


# https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m
@auth.login_excluded("/")
@xframe_options_exempt
def register_view(request):
    register_form = StyledUserCreationForm(request.POST)
    if register_form.is_valid():
        register_form.save()
        username = register_form.cleaned_data.get("username")
        password = register_form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(auth.next_path(request, True))
    return render(request, "auth/register.html", {"form": register_form})


# https://stackoverflow.com/questions/31482178/django-login-page-for-non-admin-dashboard
@auth.login_excluded("/")
@xframe_options_exempt
def login_view(request):
    login_form = StyledAuthenticationForm(request=request, data=request.POST)
    if login_form.is_valid():
        login_form.clean()
        login(request, login_form.get_user())
        return redirect(auth.next_path(request, True))
    return render(request, "auth/login.html", {"form": login_form})
