import re
import bleach
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField

from li_core import settings

cleanr = re.compile("<.*?>")


class LoginPermissions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, related_name="permissions", on_delete=models.CASCADE
    )

    no_license = models.BooleanField(default=False)


class MailProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name="mail", on_delete=models.CASCADE)

    hidden = models.BooleanField(default=False)

    def __str__(self):
        return "{username}@{domain}".format(
            username=self.user.username, domain=settings.DECORATIVE_EMAIL_DOMAIN
        )


class Email(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    content = HTMLField(default="", null=False, blank=False)
    sent_time = models.DateTimeField(auto_now_add=True, blank=True)

    sender = models.ForeignKey(
        MailProfile, related_name="sent", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        MailProfile, related_name="received", on_delete=models.CASCADE
    )

    def content_text(self) -> str:
        cleantext = re.sub(cleanr, "", self.content)

        return bleach.clean(
            cleantext,
            tags=settings.BLEACH_ALLOWED_TAGS,
            attributes=settings.BLEACH_ALLOWED_ATTRIBUTES,
            styles=settings.BLEACH_ALLOWED_STYLES,
        )

    def __str__(self):
        return 'subject:"{subject}", from:{sender}, to:{receiver}'.format(
            subject=self.title, sender=self.sender, receiver=self.receiver
        )


@receiver(post_save, sender=User)
def create_user_mail_profile(sender, instance, created, **kwargs):
    if created:
        MailProfile.objects.create(user=instance)
        LoginPermissions.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_mail_profile(sender, instance, **kwargs):
    instance.mail.save()
    instance.permissions.save()
