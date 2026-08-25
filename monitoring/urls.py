from django.urls import path

from .views import create_api, dashboard, detail_api, login_user, register_user

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("create/", create_api, name="create_api"),
    path("dashboard/<int:id>/", detail_api, name="detail_api"),
]
