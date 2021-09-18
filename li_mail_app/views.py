import bleach
from django.contrib.auth.mixins import LoginRequiredMixin
from urllib.parse import quote, unquote
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.vary import vary_on_cookie

from li_core import settings
from li_mail_app import models
from li_mail_app.forms import MailComposeForm


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

        context["reply_data"] = {
            "title": quote("RE: " + context["email"].title),
            "content": quote(
                "<br /><blockquote>" + context["content_bleached"] + "</blockquote>"
            ),
            "receiver": quote(context["email"].sender.user.username),
        }

        return context


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(xframe_options_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class MailComposeView(LoginRequiredMixin, CreateView):
    template_name = "lssrp/mail/compose.html"
    form_class = MailComposeForm
    success_url = "/mail"

    def get_initial(self):
        initial = super().get_initial()

        initial["title"] = unquote(self.request.GET.get("title", ""))
        initial["content"] = unquote(self.request.GET.get("content", ""))

        receiver = unquote(self.request.GET.get("receiver", ""))
        if receiver != "":
            initial["receiver"] = models.MailProfile.objects.get(
                user__username=receiver
            )

        return initial

    def form_valid(self, form):
        form.instance.sender = self.request.user.mail

        return super().form_valid(form)
