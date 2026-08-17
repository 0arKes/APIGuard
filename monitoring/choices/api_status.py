from django.db import models


class APIStatus(models.TextChoices):
    UP = ("UP", "Online")
    DOWN = ("DOWN", "Offline")
    UNKNOWN = ("UNKNOWN", "Unknown")
