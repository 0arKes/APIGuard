from django.contrib.auth.views import LoginView
from django.urls import path

from .forms.auth_form import LoginUserForm
from .views import register_user

app_name = "accounts"

urlpatterns = [
    path("register/", register_user, name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html", authentication_form=LoginUserForm
        ),
        name="login",
    ),
]
