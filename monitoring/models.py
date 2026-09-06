from django.contrib.auth.models import User
from django.db import models

from monitoring.choices import APIStatus

# Create your models here.


class API(models.Model):
    nickname = models.CharField(max_length=60, null=False, blank=False)
    url = models.URLField(null=False, blank=False)
    api_status = models.CharField(
        max_length=7, choices=APIStatus, default=APIStatus.UNKNOWN
    )
    timeout_count = models.PositiveSmallIntegerField(null=False, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="apis")

    def __str__(self) -> str:
        return self.nickname


class History(models.Model):
    api_response = models.CharField(max_length=30, null=False, blank=False)
    status_code = models.PositiveSmallIntegerField(null=True)
    response_time = models.PositiveSmallIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    api = models.ForeignKey(API, on_delete=models.CASCADE, related_name="histories")
