from __future__ import absolute_import, unicode_literals
from os import environ

from celery import Celery
from celery.schedules import crontab
from django.conf import settings


environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.conf.enable_utc = False

app.conf.update(timezone='Europe/Berlin')

app.config_from_object(settings, namespace='CELERY')


app.conf.beat_schedule = {
    'delete_expired_verification_codes': {
        'task': 'verification.tasks.delete_expired_verification_codes',
        'schedule': crontab(minute='*/10'),
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
