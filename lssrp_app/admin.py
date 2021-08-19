from django.contrib import admin

from lssrp_app import models


class EmailAdmin(admin.StackedInline):
    model = models.Email
    fk_name = "sender"


@admin.register(models.MailProfile)
class MailProfileAdmin(admin.ModelAdmin):
    inlines = [
        EmailAdmin
    ]

    class Meta:
        model = models.MailProfile


@admin.register(models.Email)
class EmailAdmin(admin.ModelAdmin):
    pass
