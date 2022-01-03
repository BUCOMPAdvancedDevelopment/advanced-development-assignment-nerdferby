from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile


class CustomLoginForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        fields = ["email", "password1"]


class UserRegisterForm(forms.Form):
    """
    Registers the user through django and firebase
    """
    username = forms.CharField(max_length=64)
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    address1 = forms.CharField(max_length=128, label="Address line 1")
    address2 = forms.CharField(max_length=128, required=False, label="Address line 2")
    address3 = forms.CharField(max_length=128, required=False, label="Address line 3")
    post_code = forms.CharField(max_length=128, label="Postal code")

    def save(self):
        pass

    class Meta:
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
