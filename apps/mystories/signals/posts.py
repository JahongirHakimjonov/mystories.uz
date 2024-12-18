import io
import re
import uuid

from PIL import Image
from django.core.files.base import ContentFile
from django.db.models.signals import post_save, post_delete, pre_save
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
        updated_fields = []
        if not instance.created_at:
            instance.created_at = timezone.now()
            updated_fields.append("created_at")

        if not instance.slug:
            if re.match(r"^[a-zA-Z0-9\s]+$", instance.title):
                base_slug = slugify(
                    f"{instance.title}-{instance.created_at.strftime('%Y-%m-%d')}"
                )
                unique_slug = base_slug
                num = 1
                while Post.objects.filter(slug=unique_slug).exists():
                    unique_slug = f"{base_slug}-{num}"
                    num += 1
                instance.slug = unique_slug
            else:
                instance.slug = (
                    f"{uuid.uuid4()}-{instance.created_at.strftime('%Y-%m-%d')}"
                )
            updated_fields.append("slug")

        instance.slug = instance.slug.lower()

        if updated_fields:
            instance.save(update_fields=updated_fields)


@receiver(pre_save, sender=Post)
def resize_image(sender, instance, **kwargs):
    if instance.banner and not instance.banner.name.endswith(".webp"):
        try:
            print("Converting to webp")
            instance.banner.seek(0)  # Faylni boshidan o'qishni ta'minlash
            img = Image.open(instance.banner)
            print(f"Image format: {img.format}")

            if img.format != "WEBP":
                img_io = io.BytesIO()
                img.save(img_io, format="WEBP", quality=100)
                webp_filename = f"{instance.banner.name.rsplit('.', 1)[0]}.webp"

                instance.banner.save(
                    webp_filename,
                    ContentFile(img_io.getvalue()),
                    save=False,
                )
                print(f"Saved as {webp_filename}")
        except Exception as e:
            print(f"Error converting image: {e}")
