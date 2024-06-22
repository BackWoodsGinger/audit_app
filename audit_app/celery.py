# audit_app/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audit_app.settings')

app = Celery('audit_app')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.timezone = 'America/New_York'

# Schedule to run at 6:15 PM for testing
app.conf.beat_schedule = {
    'regenerate-audits-at-specific-time': {
        'task': 'audits.tasks.regenerate_audits',
        'schedule': crontab(hour=2, minute=15),  # Run at 2:15 AM
    },
}