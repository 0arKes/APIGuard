from django.urls import path

from .views import CreateAPI, Dashboard, DetailAPI

app_name = "monitoring"

urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("create/", CreateAPI.as_view(), name="create_api"),
    path("dashboard/<int:id>/", DetailAPI.as_view(), name="detail_api"),
]
