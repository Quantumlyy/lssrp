from django.core.handlers.wsgi import WSGIRequest
from django.utils.http import is_safe_url

from lssrp_core import settings


def next(request: WSGIRequest):
    nxt = request.GET.get("next", None)
    if nxt is None:
        return settings.LOGIN_REDIRECT_URL
    elif not is_safe_url(
        url=nxt, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return settings.LOGIN_REDIRECT_URL
    else:
        return nxt
