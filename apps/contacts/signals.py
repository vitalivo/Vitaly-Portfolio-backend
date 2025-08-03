from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ContactMessage
from .utils import send_contact_notification
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ContactMessage)
def contact_message_created(sender, instance, created, **kwargs):
    """
    Автоматически отправляем уведомления при создании нового сообщения
    """
    if created:  # Только для новых сообщений
        try:
            # Отправляем уведомления (Email + Telegram)
            send_contact_notification(instance)
            logger.info(f"Notifications sent for contact message: {instance.id}")
        except Exception as e:
            logger.error(f"Failed to send notifications for contact message {instance.id}: {str(e)}")
