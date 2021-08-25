from django.contrib import admin

from lssrp_app import models


class EmailSentAdmin(admin.StackedInline):
    model = models.Email
    fk_name = "sender"
    verbose_name_plural = "Sent emails"


class EmailReceivedAdmin(admin.StackedInline):
    model = models.Email
    fk_name = "receiver"
    verbose_name_plural = "Received emails"


@admin.register(models.MailProfile)
class MailProfileAdmin(admin.ModelAdmin):
    inlines = [EmailSentAdmin, EmailReceivedAdmin]

    class Meta:
        model = models.MailProfile


@admin.register(models.Email)
class EmailAdmin(admin.ModelAdmin):
    pass
