from django import forms


class OrderForm(forms.Form):
    customer = forms.EmailField()
    product_id = forms.CharField(max_length=16)


# class CustomLoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.PasswordInput()
#
#     class Meta:
#         fields = ["email", "password"]
#
#
# class UserRegisterForm(UserCreationForm):
#     """
#     Registers the user through django and firebase
#     """
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]
#
#
# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ["username", "email"]
#
#
# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ["avatar"]
