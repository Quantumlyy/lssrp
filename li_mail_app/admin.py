from django.contrib import admin
from django.utils.translation import gettext as _

from li_mail_app import models


class EmailSentAdmin(admin.StackedInline):
    model = models.Email
    fk_name = "sender"
    verbose_name_plural = _("Sent emails")


class EmailReceivedAdmin(admin.StackedInline):
    model = models.Email
    fk_name = "receiver"
    verbose_name_plural = _("Received emails")


@admin.register(models.MailProfile)
class MailProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "hidden"]
    inlines = [EmailSentAdmin, EmailReceivedAdmin]


@admin.register(models.Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ["title", "sender", "receiver", "sent_time"]
