from django.db import models

from django.conf import settings
from django.contrib.auth import get_user_model
from authentications.models import CustomUser
from django.utils import timezone

class TaskProject(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank = True, null = True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in progress', 'In progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(TaskProject, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank = True, null = True, related_name='user')

    def __str__(self):
        return self.title
    
class Statusholder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank = True, null = True)
    status = models.ForeignKey(Task, on_delete=models.CASCADE)
    
    
