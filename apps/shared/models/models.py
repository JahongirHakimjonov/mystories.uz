from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created at"), db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated at"), db_index=True
    )

    class Meta:
        abstract = True


class Country(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Country"), db_index=True)
    code = models.CharField(max_length=4, verbose_name=_("Country code"), db_index=True)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countrys")
        db_table = "countries"
        ordering = ["name"]

    def __str__(self):
        return self.name
