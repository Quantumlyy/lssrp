from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import CreateView
from django.views.generic.base import View

from li_core import settings
from li_shared_app.forms import StyledUserCreationForm, StyledAuthenticationForm
from li_shared_app.utils import auth


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
