import io

from PIL import Image
from django.core.files.base import ContentFile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify

from apps.mystories.models import Like, Comment, Saved
from apps.mystories.models import Post


@receiver(post_save, sender=Like)
def increment_like_count(sender, instance, created, **kwargs):  # noqa
    if created:
        instance.post.like_count += 1
        instance.post.save()


@receiver(post_delete, sender=Like)
def decrement_like_count(sender, instance, **kwargs):  # noqa
    instance.post.like_count -= 1
    instance.post.save()


@receiver(post_save, sender=Comment)
def increment_comment_count(sender, instance, created, **kwargs):  # noqa
    if created:
        instance.post.comment_count += 1
        instance.post.save()


@receiver(post_delete, sender=Comment)
def decrement_comment_count(sender, instance, **kwargs):  # noqa
    instance.post.comment_count -= 1
    instance.post.save()


@receiver(post_save, sender=Saved)
def increment_saved_count(sender, instance, created, **kwargs):  # noqa
    if created:
        instance.post.saved_count += 1
        instance.post.save()


@receiver(post_delete, sender=Saved)
def decrement_saved_count(sender, instance, **kwargs):  # noqa
    instance.post.saved_count -= 1
    instance.post.save()


@receiver(post_save, sender=Post)
def post_save_post(sender, instance, created, **kwargs):
    if created:
        if not instance.created_at:
            instance.created_at = timezone.now()
        if not instance.slug:
            instance.slug = slugify(
                f"{instance.title}-{instance.created_at.strftime('%Y-%m-%d')}"
            )
            unique_slug = instance.slug
            num = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{instance.slug}-{num}"
                num += 1
            instance.slug = unique_slug
        instance.slug = instance.slug.lower()
        instance.save()
    if instance.pk:
        old_instance = Post.objects.get(pk=instance.pk)
        if old_instance.banner != instance.banner:
            if instance.banner:
                img = Image.open(instance.banner)
                if img.format != "WEBP":
                    img_io = io.BytesIO()
                    img.save(img_io, format="WEBP", quality=100)
                    instance.banner.save(
                        f"{instance.banner.name.split('.')[0]}.webp",
                        ContentFile(img_io.getvalue()),
                        save=False,
                    )
