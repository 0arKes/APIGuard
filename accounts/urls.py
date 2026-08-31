from django.contrib.auth.views import LoginView
from django.urls import path

from .forms.auth_form import LoginUserForm
from .views import Logout, RegisterUser

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html", authentication_form=LoginUserForm
        ),
        name="login",
    ),
    path("logout/", Logout.as_view(), name="logout"),
]
