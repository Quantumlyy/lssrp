from django.contrib.auth.decorators import user_passes_test
from django.core.handlers.wsgi import WSGIRequest
from django.utils.http import is_safe_url
from django.shortcuts import redirect

from lssrp_core import settings


def next_path(request: WSGIRequest, force: bool):
    nxt = request.GET.get("next", None)
    if nxt is None:
        return settings.LOGIN_REDIRECT_URL
    elif (
        not is_safe_url(
            url=nxt,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )
        and not force
    ):
        return settings.LOGIN_REDIRECT_URL
    else:
        return nxt


# https://stackoverflow.com/questions/18558636/redirect-if-already-logged-in-through-django-urls/18558770
login_forbidden = user_passes_test(
    lambda u: u.is_anonymous(), settings.LOGIN_REDIRECT_URL
)


# https://newbedev.com/how-to-prevent-user-to-access-login-page-in-django-when-already-logged-in
def login_excluded(redirect_to):
    """This decorator kicks authenticated users out of a view"""

    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper
