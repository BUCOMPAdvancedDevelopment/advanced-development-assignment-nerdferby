from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile
from firebase_admin import auth


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            user = auth.create_user(
                email=self.email,
                email_verified=False,
                password=super().clean_password2(),
                display_name='',
                photo_url='',
                disabled=False
            )
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
