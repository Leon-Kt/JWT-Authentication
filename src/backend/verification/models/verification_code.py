from django.db import models
from django.utils import timezone


class VerificationCode(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)

    def is_valid(self):
        expiration_time = timezone.timedelta(hours=2)
        return self.created_at + expiration_time > timezone.now()

    class Meta:
        app_label = 'verification'
