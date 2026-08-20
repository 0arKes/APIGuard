from django.urls import path

from .views import dashboard, login_user, register_user

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
]
