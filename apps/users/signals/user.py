from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.mystories.models import Notification
from apps.users.models import ActiveSessions


@receiver(post_save, sender=ActiveSessions)
def increment_active_sessions(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            title_uz="Yangi qurilma orqali kirdingiz",
            title_ru="Вы вошли с нового устройства",
            title_en="You have logged in from a new device",
            message_uz="Siz yangi qurilma orqali kirdingiz.",
            message_ru="Вы вошли с нового устройства.",
            message_en="You have logged in from a new device.",
        )
