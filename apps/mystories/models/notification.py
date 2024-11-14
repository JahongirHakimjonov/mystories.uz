from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Notification(AbstractBaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("User"),
    )
    title = models.CharField(max_length=255, db_index=True, verbose_name=_("Title"))
    message = models.TextField(db_index=True, verbose_name=_("Message"))
    is_send = models.BooleanField(default=False, verbose_name=_("Is Send"))
    is_read = models.BooleanField(default=False, verbose_name=_("Is Read"))

    class Meta:
        db_table = "notifications"
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ["-created_at"]

    def __str__(self):
        return self.message
