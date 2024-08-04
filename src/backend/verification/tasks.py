from django.utils import timezone
from celery import shared_task

from verification.models import VerificationCode


@shared_task
def delete_expired_verification_codes():
    expired_codes = VerificationCode.objects.filter(created_at__lte=timezone.now() - timezone.timedelta(minutes=30))
    expired_codes.delete()
