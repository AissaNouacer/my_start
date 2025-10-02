"""
Celery configuration for delivery_platform project.
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_platform.settings')

# Create Celery instance
app = Celery('delivery_platform')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django app configs
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'cleanup-expired-sessions': {
        'task': 'apps.common.tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    'update-driver-ratings': {
        'task': 'apps.users.tasks.update_driver_ratings',
        'schedule': crontab(hour=3, minute=0),  # Daily at 3 AM
    },
    'check-low-stock-products': {
        'task': 'apps.stores.tasks.check_low_stock_products',
        'schedule': crontab(minute=0),  # Every hour
    },
    'update-store-metrics': {
        'task': 'apps.stores.tasks.update_all_store_metrics',
        'schedule': crontab(hour=4, minute=0),  # Daily at 4 AM
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
