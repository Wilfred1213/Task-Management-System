# celerybeat.py

import os
from celery import Celery
import django
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Task_management_system.settings')
django.setup()

app = Celery('Task_management_system')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'send-reminder-emails': {
        # 'task': 'task.tasks.send_reminder_emails',
        # 'schedule': 10,  # Run the task every 60 seconds
        # 'schedule': timedelta(weeks=1),  # Run the task once a week
        'schedule': 2 * 24 * 60 * 60,  # 2 days in seconds

    },
}
