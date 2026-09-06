from django.contrib import admin

from .models import API, History

# Register your models here.


@admin.register(API)
class APIAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nickname",
        "url",
        "api_status",
        "timeout_count",
        "owner",
    )

    list_filter = ("api_status",)
    ordering = ("id",)
    list_per_page = 10

    readonly_fields = (
        "id",
        "api_status",
        "timeout_count",
    )


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "api_response",
        "status_code",
        "response_time",
        "date",
        "api",
    )

    ordering = ("id",)
    list_per_page = 10

    readonly_fields = (
        "id",
        "api_response",
        "status_code",
        "response_time",
        "date",
        "api",
    )
