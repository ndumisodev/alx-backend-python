# messaging/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification
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
    """
    Logs old content of a message before it is updated
    """
    if instance.pk:  # means the message already exists
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return  # message not found in DB

        # Check if content actually changed
        if old_message.content != instance.content:
            # Save history
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content
            )

            # Mark message as edited
            instance.edited = True