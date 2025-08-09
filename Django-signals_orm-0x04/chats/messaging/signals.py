# messaging/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification
from .models import Message, MessageHistory

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory




@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        
        if old_message.content != instance.content:
            # Log the old content with info who edited (use instance.sender or request user if accessible)
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content,
                edited_by=instance.sender  # assuming sender is the editor here
            )
            instance.edited = True
