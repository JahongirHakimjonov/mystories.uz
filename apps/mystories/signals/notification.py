import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.mystories.models import Notification
from apps.mystories.tasks import send_notification_task

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):  # noqa
    if created:
        send_notification_task.delay(instance.id)
