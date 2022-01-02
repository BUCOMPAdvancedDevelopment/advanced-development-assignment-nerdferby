from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.exceptions import ValidationError
from firebase_admin import auth
from firebase_admin.exceptions import PermissionDeniedError

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CustomLoginForm
from AdvancedDevelopment.firebase import add_data, get_all_data


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            add_data(u'users', str(data["username"]), data)
            messages.success(
                request, f"Form valid. Username is {data['username']}. User not created"
            )
            # form.save()
            # messages.success(
            #     request, "Your account has been created! You can now log in."
            # )
            # return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        # todo sanitise inputs
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            messages.success(request, "Login successful!")
        else: 
            messages.error(request, "Failed to login!")
    else:
        form = CustomLoginForm()
    return render(request, "users/login.html")


# class DeactivateUser(View):
#     def get(self, request):
#         return render(request, "users/profile_deactivate_confirm.html")
#
#     def post(self, request):
#         try:
#             user = User.objects.get(username=request.user.username)
#             user.is_active = False
#             user.save()
#             messages.success(request, f"Account {user.username} has been disabled!")
#         except User.DoesNotExist:
#             messages.error(request, "Account does not exist")
#         except Exception as e:
#             messages.error(request, e.message)
#
#         # return render(request, "users/profile_deactivate_confirm.html", context=context)
#         return redirect("/")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {"u_form": u_form,
                   "p_form": p_form
                   }
        return render(request, "users/profile.html", context)

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect("profile")
