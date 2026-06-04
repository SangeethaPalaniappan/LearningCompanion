from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from .models import Users


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or email")

    def clean(self):
        identifier = self.cleaned_data.get("username")
        user = None

        if identifier and "@" in identifier:
            User = get_user_model()
            user = User.objects.filter(email__iexact=identifier).first()

            if user is None:
                users_record = Users.objects.filter(mail_id__iexact=identifier).first()
                if users_record:
                    user = User.objects.filter(username=users_record.user_name).first()

        if user:
            self.cleaned_data["username"] = user.get_username()

        return super().clean()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data["email"]

        if Users.objects.filter(mail_id=email).exists():
            raise forms.ValidationError("An account with this email already exists.")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user
