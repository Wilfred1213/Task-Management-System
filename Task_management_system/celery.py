# celery.py

import os
from celery import Celery
import django

# Set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Task_management_system.settings')
django.setup()

app = Celery('Task_management_system')

# Load celery settings from Django settings module
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in all Django apps
app.autodiscover_tasks()
