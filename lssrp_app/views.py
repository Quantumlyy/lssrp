import bleach
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template import Template, Context
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.vary import vary_on_cookie

from lssrp_core import settings
from lssrp_app import models
from lssrp_app.forms import (
    StyledUserCreationForm,
    StyledAuthenticationForm,
    MailComposeForm,
)
from lssrp_app.utils import auth


@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class HomeView(TemplateView):
    template_name = "lssrp/base.html"


@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class MailView(TemplateView):
    template_name = "lssrp/mail/home.html"
    model = models.MailProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profile"] = models.MailProfile.objects.get(user=self.request.user)
        context["target"] = models.Email.objects.filter(receiver=context["profile"])
        context["sent"] = False

        return context


@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class MailSentView(TemplateView):
    template_name = "lssrp/mail/home.html"
    model = models.MailProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profile"] = models.MailProfile.objects.get(user=self.request.user)
        context["target"] = models.Email.objects.filter(sender=context["profile"])
        context["sent"] = True

        return context


@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
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

        context["content_bleached"] = bleach.clean(
            context["email"].content,
            tags=settings.BLEACH_ALLOWED_TAGS,
            attributes=settings.BLEACH_ALLOWED_ATTRIBUTES,
            styles=settings.BLEACH_ALLOWED_STYLES,
        )

        return context


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class MailComposeView(LoginRequiredMixin, CreateView):
    template_name = "lssrp/mail/compose.html"
    form_class = MailComposeForm
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


@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(auth.login_excluded("/"), name="dispatch")
class RegisterView(CreateView):
    template_name = "auth/register.html"
    form_class = StyledUserCreationForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return redirect(auth.next_path(self.request, True))


@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(auth.login_excluded("/"), name="dispatch")
class LoginView(LoginView):
    template_name = "auth/login.html"
    form_class = StyledAuthenticationForm

    def form_valid(self, form):
        form.clean()
        login(self.request, form.get_user())

        return redirect(auth.next_path(self.request, True))
