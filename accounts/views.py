from django.shortcuts import redirect, render
from django.views import View

from .forms.auth_form import CreateUserForm
from .services.user_services import create_user

# Create your views here.


class RegisterUser(View):
    def get(self, request):
        form_user = CreateUserForm()
        return render(request, "accounts/register.html", {"form": form_user})

    def post(self, request):
        form_user = CreateUserForm(request.POST)

        if form_user.is_valid():
            create_user(
                username=form_user.cleaned_data["username"],
                email=form_user.cleaned_data["email"],
                password=form_user.cleaned_data["password"],
            )

            return redirect("accounts:login")

        return render(request, "accounts/register.html", {"form": form_user})
