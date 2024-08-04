from django.db import models
from django.utils import timezone


class RefreshToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token
