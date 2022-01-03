from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

# from AdvancedDevelopment.firebase import add_data, get_all_data
from AdvancedDevelopment.firebase import FirebaseClient
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CustomLoginForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            firebase = FirebaseClient("users")
            firebase.create(document=str(data["username"]), data=data)
            messages.success(
                request, f"Form valid. Username is {data['username']}. User not created"
            )
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def _login_validation(firebase_client: FirebaseClient, form: CustomLoginForm):
    """
    Checks the entered login details against the database user records
    :param firebase_client: Firebase client connecting to users collection
    :param form: the custom login form containing login information
    :return: if password entered matches stored password, the result of the query to find the user
    """
    if form.is_valid():
        query = firebase_client.filter("email", "==", form.cleaned_data["email"])
        user_found = False
        try:
            user_found = query[0]
        except IndexError:  # Invalid login, user does not exist
            return False, user_found
        password_match = user_found["password2"] == form.cleaned_data["password1"]
        return password_match, user_found
    else:
        return False, False


def login(request):
    try:
        messages.warning(request, f"You are already logged in as, {request.session['login']}")
    except KeyError:
        pass
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            client = FirebaseClient("users")
            password_match, user_found = _login_validation(client, form)
            if password_match:
                request.session["login"] = user_found["username"]
                messages.success(request, f"Successful login as, {form.cleaned_data['email']}")
            else:
                messages.error(request, "You have entered the wrong login credentials!")
        else:
            messages.error(request, "Failed to login!")
    else:
        form = CustomLoginForm()
    return render(request, "users/login.html", {"form": form})


def logout(request):
    session: str
    try:
        request.session.pop("login")
        messages.success(request, "You have been successfully logged out")
        return redirect(login)
    except KeyError:  # user is not logged in, redirect to login page
        return redirect(login)


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
