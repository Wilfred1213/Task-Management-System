from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from task.models import Task
from django.utils.html import strip_tags

@receiver(post_save, sender=Task)
def send_task_assignment_email(sender, instance, created, **kwargs):
    if created:
        # Task was created, send email notification
        subject = 'Task Assignment'
        message = f"You have been assigned a new task:\n\nTitle: {instance.title}\nDescription: {instance.description}\nDue Date: {instance.due_date}"
        recipient_list = [instance.assigned_to.email]  # Assuming assigned_to field is a ForeignKey to CustomUser model with an email field
        sender_email = 'mathiaswilfred7@gmail.com'  # Set the sender email address
        send_mail(subject, message, sender_email, recipient_list)

        
