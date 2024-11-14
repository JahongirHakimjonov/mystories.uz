from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.mystories.models import Like, Comment, Saved


@receiver(post_save, sender=Like)
def increment_like_count(sender, instance, created, **kwargs):
    if created:
        instance.post.like_count += 1
        instance.post.save()


@receiver(post_delete, sender=Like)
def decrement_like_count(sender, instance, **kwargs):
    instance.post.like_count -= 1
    instance.post.save()


@receiver(post_save, sender=Comment)
def increment_comment_count(sender, instance, created, **kwargs):
    if created:
        instance.post.comment_count += 1
        instance.post.save()


@receiver(post_delete, sender=Comment)
def decrement_comment_count(sender, instance, **kwargs):
    instance.post.comment_count -= 1
    instance.post.save()


@receiver(post_save, sender=Saved)
def increment_saved_count(sender, instance, created, **kwargs):
    if created:
        instance.post.saved_count += 1
        instance.post.save()


@receiver(post_delete, sender=Saved)
def decrement_saved_count(sender, instance, **kwargs):
    instance.post.saved_count -= 1
    instance.post.save()
