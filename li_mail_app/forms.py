from django.contrib.auth.forms import (
    UserCreationForm,
    UsernameField,
    AuthenticationForm,
)
from django.forms import TextInput, CharField, PasswordInput, ModelForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import (
    get_user_model,
    password_validation,
)
from django.db.models import Q

from li_mail_app import models


class StyledUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2")

    username = UsernameField(
        widget=TextInput(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            }
        )
    )
    password1 = CharField(
        label=_("Password"),
        strip=False,
        widget=PasswordInput(
            attrs={
                "class": "shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = CharField(
        label=_("Password confirmation"),
        widget=PasswordInput(
            attrs={
                "class": "shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            }
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")

        if username and "@" in username:
            # TODO: translation
            msg = "Uporabniško ime ne vključuje domene."
            self.add_error("username", msg)


class StyledAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        widget=TextInput(
            attrs={
                "autofocus": True,
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            }
        )
    )
    password = CharField(
        label=_("Password"),
        strip=False,
        widget=PasswordInput(
            attrs={
                "class": "shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            }
        ),
    )


class MailComposeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MailComposeForm, self).__init__(*args, **kwargs)
        self.fields["receiver"].queryset = models.MailProfile.objects.filter(
            hidden=False
        )

    class Meta:
        model = models.Email
        fields = ["receiver", "title", "content"]
