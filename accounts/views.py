from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms.auth_form import CreateUserForm

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

        return render(request, "accounts/register.html", {"form": form_user})

    return render(request, "accounts/register.html", {"form": form_user})
