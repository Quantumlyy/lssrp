"""sportaj_core URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import lssrp_app.views
from lssrp_core import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login_required(lssrp_app.views.HomeView.as_view()), name="home"),
    path("mail/", login_required(lssrp_app.views.MailView.as_view()), name="mail"),
    path(
        "mail/folder/in/",
        login_required(lssrp_app.views.MailView.as_view()),
        name="mail",
    ),
    path(
        "mail/folder/out/",
        login_required(lssrp_app.views.MailSentView.as_view()),
        name="mail_sent",
    ),
    path(
        "mail/email/<int:pk>",
        login_required(lssrp_app.views.EmailView.as_view()),
        name="email",
    ),
    path(
        "mail/compose/",
        login_required(lssrp_app.views.MailComposeView.as_view()),
        name="mail_compose",
    ),
    path("prijava/", lssrp_app.views.login_view, name="login"),
    path("registracija/", lssrp_app.views.register_view, name="register"),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
