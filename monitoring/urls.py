from django.urls import path

from .views import create_api, dashboard, login_user, register_user

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("create/", create_api, name="create_api"),
]
