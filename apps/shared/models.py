from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Yaratilgan sana")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("O'zgartirilgan sana")
    )

    class Meta:
        abstract = True


class Country(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Davlat nomi"))
    code = models.CharField(max_length=4, verbose_name=_("Davlat kodi"))

    class Meta:
        verbose_name = _("Davlat")
        verbose_name_plural = _("Davlatlar")

    def __str__(self):
        return self.name
