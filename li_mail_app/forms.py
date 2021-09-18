from django.forms import ModelForm

from li_mail_app import models


class MailComposeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MailComposeForm, self).__init__(*args, **kwargs)
        self.fields["receiver"].queryset = models.MailProfile.objects.filter(
            hidden=False
        )

    class Meta:
        model = models.Email
        fields = ["receiver", "title", "content"]
