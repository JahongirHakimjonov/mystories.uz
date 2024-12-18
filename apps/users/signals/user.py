import io

from PIL import Image
from django.core.files.base import ContentFile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.mystories.models import Notification, NotificationType
from apps.users.models import ActiveSessions, User


@receiver(post_save, sender=ActiveSessions)
def increment_active_sessions(sender, instance, created, **kwargs):  # noqa
    if created:
        address = f"{instance.location.get('country', '')}, {instance.location.get('city', '')}"
        latitude = instance.location.get("lat", "")
        longitude = instance.location.get("lon", "")
        coordinates = f"{latitude}, {longitude}"
        ip = instance.ip
        device = instance.user_agent
        isp = instance.location.get("isp", "")
        timezone = instance.location.get("timezone", "")
        created_at = instance.created_at.strftime("%Y-%m-%d  %H:%M:%S")

        messages = {
            "uz": f"Akkauntizga soat {created_at} da {address} dan kirildi, Kordinatalar: {coordinates}, IP: {ip}, Qurilma: {device}, ISP: {isp}, Timezone: {timezone}",
            "ru": f"Ваш аккаунт был вошел в {created_at} из {address}, Координаты: {coordinates}, IP: {ip}, Устройство: {device}, ISP: {isp}, Timezone: {timezone}",
            "en": f"Your account was logged in at {created_at} from {address}, Coordinates: {coordinates}, IP: {ip}, Device: {device}, ISP: {isp}, Timezone: {timezone}",
        }

        Notification.objects.create(
            user_id=instance.user_id,
            title_uz="Yangi kirish",
            title_ru="Новый вход",
            title_en="New login",
            message_uz=messages["uz"],
            message_ru=messages["ru"],
            message_en=messages["en"],
            type=NotificationType.SINGLE,
        )


@receiver(pre_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    if instance.avatar and not instance.avatar.name.endswith(".webp"):
        try:
            print("Converting to webp")
            instance.avatar.seek(0)  # Faylni boshidan o'qishni ta'minlash
            img = Image.open(instance.avatar)
            print(f"Image format: {img.format}")

            if img.format != "WEBP":
                img_io = io.BytesIO()
                img.save(img_io, format="WEBP", quality=100)
                webp_filename = f"{instance.avatar.name.rsplit('.', 1)[0]}.webp"

                instance.avatar.save(
                    webp_filename,
                    ContentFile(img_io.getvalue()),
                    save=False,
                )
                print(f"Saved as {webp_filename}")
        except Exception as e:
            print(f"Error converting image: {e}")
