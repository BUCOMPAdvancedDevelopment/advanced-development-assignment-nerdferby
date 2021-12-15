from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile
from firebase_admin import auth


class UserRegisterForm(UserCreationForm):
    """
    Registers the user through django and firebase
    """
    email = forms.EmailField()

    def __init__(self, post=None, *args, **kwargs):
        if post is not None:
            self._email = post["email"]
            self._password = post["password2"]
        # self._password = password2
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        print(f"{self._email}")
        email = self._email
        clean_password = self._password
        try:
            user = auth.create_user(
                email=email,
                email_verified=False,
                password=clean_password)
            super().save(*args, **kwargs)
            print('Successfully created new user: {0}'.format(user.uid))
        except ValidationError as error:
            print(error.message)

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
