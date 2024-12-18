from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class NotificationType(models.TextChoices):
    SINGLE = "SINGLE", _("Single")
    ALL = "ALL", _("All")


class Notification(AbstractBaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("User"),
    )
    banner = models.FileField(
        upload_to="notifications",
        null=True,
        blank=True,
        verbose_name=_("Banner"),
    )
    title = models.CharField(max_length=255, db_index=True, verbose_name=_("Title"))
    message = models.TextField(db_index=True, verbose_name=_("Message"))
    is_send = models.BooleanField(default=False, verbose_name=_("Is Send"))
    is_read = models.BooleanField(default=False, verbose_name=_("Is Read"))
    type = models.CharField(
        max_length=10,
        choices=NotificationType,
        default=NotificationType.SINGLE,
        verbose_name=_("Type"),
    )

    class Meta:
        db_table = "notifications"
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ["-created_at"]

    def __str__(self):
        return self.message
