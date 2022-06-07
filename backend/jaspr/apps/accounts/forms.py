from django.contrib.auth import forms
from django.core.exceptions import ValidationError

from .models import User


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        # Removes `{"username": ...}` from the `field_classes` of the parent class.
        field_classes = {}


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_email": "This email has already been taken."}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        # Removes `{"username": ...}` from the `field_classes` of the parent class.
        field_classes = {}

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise ValidationError(self.error_messages["duplicate_email"])
