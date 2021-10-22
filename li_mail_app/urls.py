from django.urls import path

from li_mail_app import views

urlpatterns = [
    path(
        "",
        views.HomeView.as_view(),
        name="home",
    ),
    path(
        "mail/",
        views.MailView.as_view(),
        name="mail",
    ),
    path(
        "mail/folder/in/",
        views.MailView.as_view(),
        name="mail",
    ),
    path(
        "mail/folder/out/",
        views.MailSentView.as_view(),
        name="mail_sent",
    ),
    path(
        "mail/email/<int:pk>",
        views.EmailView.as_view(),
        name="email",
    ),
    path(
        "mail/compose/",
        views.MailComposeView.as_view(),
        name="mail_compose",
    ),
]
