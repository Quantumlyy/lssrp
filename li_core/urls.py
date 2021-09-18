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
from django.urls import path, include

import li_mail_app.views
from li_core import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path(
        "",
        li_mail_app.views.HomeView.as_view(),
        name="home",
    ),
    path(
        "mail/",
        li_mail_app.views.MailView.as_view(),
        name="mail",
    ),
    path(
        "mail/folder/in/",
        li_mail_app.views.MailView.as_view(),
        name="mail",
    ),
    path(
        "mail/folder/out/",
        li_mail_app.views.MailSentView.as_view(),
        name="mail_sent",
    ),
    path(
        "mail/email/<int:pk>",
        li_mail_app.views.EmailView.as_view(),
        name="email",
    ),
    path(
        "mail/compose/",
        li_mail_app.views.MailComposeView.as_view(),
        name="mail_compose",
    ),
    path("prijava/", li_mail_app.views.LoginView.as_view(), name="login"),
    path("registracija/", li_mail_app.views.RegisterView.as_view(), name="register"),
    path("odjava/", li_mail_app.views.LogoutView.as_view(), name="logout"),
    path("close/", li_mail_app.views.CloseView.as_view(), name="close"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
