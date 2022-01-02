from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile


class CustomLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()

    class Meta:
        fields = ["email", "password"]


class UserRegisterForm(UserCreationForm):
    """
    Registers the user through django and firebase
    """
    email = forms.EmailField()

    class Meta:
        model = User
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
