from celery import shared_task
from django.core.mail import send_mail

from datetime import date


@shared_task
def send_reminder_emails():
    from task.models import Task
    today = date.today()
    tasks = Task.objects.filter(due_date__gte=today)  # Filter tasks with due date greater than or equal to today
    for task in tasks:
        user = task.assigned_to
        subject = 'Task Reminder: {}'.format(task.title)
        message = 'This is a reminder for your task: {}'.format(task.title)
        send_mail(subject, message, 'mathiaswilfred7@yahoo.com', [user.email])
