import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_platform.settings.dev')

app = Celery('delivery_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
