from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.users.models import Follower


@receiver(post_save, sender=Follower)
def increment_follow_counts(sender, instance, created, **kwargs):
    if created:
        instance.follower.following_count += 1
        instance.follower.save()
        instance.following.follower_count += 1
        instance.following.save()


@receiver(post_delete, sender=Follower)
def decrement_follow_counts(sender, instance, **kwargs):
    instance.follower.following_count -= 1
    instance.follower.save()
    instance.following.follower_count -= 1
    instance.following.save()
