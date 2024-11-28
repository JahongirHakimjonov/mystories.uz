import io

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Theme(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"), db_index=True)
    image = models.ImageField(
        upload_to="themes/", verbose_name=_("Image"), blank=True, null=True
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")
        db_table = "themes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"ID:{self.id} - {self.name}"

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            if img.format != "WEBP":
                img_io = io.BytesIO()
                img.save(img_io, format="WEBP", quality=100)
                self.image.save(
                    f"{self.image.name.split('.')[0]}.webp",
                    ContentFile(img_io.getvalue()),
                    save=False,
                )
        super().save(*args, **kwargs)


class Tag(AbstractBaseModel):
    theme = models.ForeignKey(
        "Theme",
        on_delete=models.CASCADE,
        related_name="tags",
        verbose_name=_("Theme"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Name"), db_index=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        db_table = "tags"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
