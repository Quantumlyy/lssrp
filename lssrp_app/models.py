from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class MailProfile(models.Model):
    user = models.OneToOneField(User, related_name="mail", on_delete=models.CASCADE)


class Email(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(null=True, blank=True)
    sent_time = models.DateField()

    sender = models.ForeignKey(
        MailProfile, related_name="sent", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        MailProfile, related_name="received", on_delete=models.CASCADE
    )


@receiver(post_save, sender=User)
def create_user_mail_profile(sender, instance, created, **kwargs):
    if created:
        MailProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_mail_profile(sender, instance, **kwargs):
    instance.mail.save()
