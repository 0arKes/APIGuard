from django.contrib.auth.models import User
from django.shortcuts import render

from .forms.login_form import CreateUserForm


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

        return render(request, "monitoring/login.html", {"form": form_user})

    return render(request, "monitoring/login.html", {"form": form_user})
