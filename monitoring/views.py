from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms.login_form import CreateUserForm, LoginUserForm


# Create your views here.
def register_user(request):

    form_user = CreateUserForm()

    if request.method == "POST":
        form_user = CreateUserForm(request.POST)
        if form_user.is_valid():
            form = form_user.cleaned_data
            User.objects.create_user(
                username=form["username"],
                email=form["email"],
                password=form["password"],
            )
            return redirect("login")

        return render(request, "monitoring/register.html", {"form": form_user})

    return render(request, "monitoring/register.html", {"form": form_user})


def login_user(request):
    login_form = LoginUserForm()

    if request.method == "POST":
        login_form = LoginUserForm(request.POST)

        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data["username"],
                password=login_form.cleaned_data["password"],
            )

            if user is None:
                login_form.add_error(None, "Credenciais Invalidas")

            else:
                login(request, user)

    return render(request, "monitoring/login.html", {"form": login_form})
