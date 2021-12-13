from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    """
    @param request: Required to set up the view
    @return: Renders the form and redirects from register page to login on POST
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your account has been created! You can now log in."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


class DeactivateUser(View):
    def get(self, request):
        return render(request, "users/profile_deactivate_confirm.html")

    def post(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            user.is_active = False
            user.save()
            messages.success(request, f"Account {user.username} has been disabled!")
        except User.DoesNotExist:
            messages.error(request, "Account does not exist")
        except Exception as e:
            messages.error(request, e.message)

        # return render(request, "users/profile_deactivate_confirm.html", context=context)
        return redirect("/")


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
