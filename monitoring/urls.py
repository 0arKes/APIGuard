from django.urls import path

from .views import create_api, dashboard, detail_api

app_name = "monitoring"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("create/", create_api, name="create_api"),
    path("dashboard/<int:id>/", detail_api, name="detail_api"),
]
