from django.urls import path

from .views import CreateAPI, Dashboard, DeleteAPI, DetailAPI, EditAPI

app_name = "monitoring"

urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("create/", CreateAPI.as_view(), name="create_api"),
    path("dashboard/<int:id>/", DetailAPI.as_view(), name="detail_api"),
    path("dashboard/edit/<int:id>/", EditAPI.as_view(), name="edit_api"),
    path("dashboard/delete/<int:id>/", DeleteAPI.as_view(), name="delete_api"),
]
