from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from verified_email_field.forms import VerifiedEmailField

from .models import ReviewUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = ReviewUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = ReviewUser
        fields = ('username', 'email')


class RegistrationForm(forms.ModelForm):
    email = VerifiedEmailField(
        label='email',
        fieldsetup_id='registration-form-email',
        required=True
    )