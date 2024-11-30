from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import ActiveSessions
from apps.users.tasks import create_map_screenshot_and_notify


@receiver(post_save, sender=ActiveSessions)
def increment_active_sessions(sender, instance, created, **kwargs):
    if created:
        create_map_screenshot_and_notify.delay(instance.id)
