from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Follower(AbstractBaseModel):
    follower = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="followers",
        verbose_name=_("Follower"),
    )
    following = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="followings",
        verbose_name=_("Following"),
    )

    class Meta:
        verbose_name = _("Follower")
        verbose_name_plural = _("Followers")
        unique_together = ["follower", "following"]
        ordering = ["-created_at"]
        db_table = "followers"

    def __str__(self):
        return f"{self.follower} -> {self.following}"
