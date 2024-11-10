import io

from PIL import Image
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.models import AbstractBaseModel
from apps.users.managers import UserManager


class RoleChoices(models.TextChoices):
    ADMIN = "ADMIN", _("Admin")
    USER = "USER", _("Foydalanuvchi")
    MODERATOR = "MODERATOR", _("Moderator")


class RegisterTypeChoices(models.TextChoices):
    EMAIL = "EMAIL", _("Email orqali")
    GOOGLE = "GOOGLE", _("Google orqali")
    GITHUB = "GITHUB", _("Github orqali")


class User(AbstractUser, AbstractBaseModel):
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email"),
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Foydalanuvchi nomi"),
    )
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, verbose_name=_("Avatar")
    )
    is_active = models.BooleanField(
        default=False,
        help_text=_(
            "Bu foydalanuvchini faol deb hisoblash kerakligini belgilaydi. Hisoblarni o'chirish o'rniga bu belgini olib tashlang."
        ),
    )
    role = models.CharField(
        choices=RoleChoices.choices,
        max_length=20,
        default=RoleChoices.USER,
        verbose_name=_("Role"),
    )
    country = models.ForeignKey(
        "shared.Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Davlat"),
    )
    register_type = models.CharField(
        choices=RegisterTypeChoices.choices,
        max_length=20,
        default=RegisterTypeChoices.EMAIL,
        verbose_name=_("Ro'yxatdan o'tish turi"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="custom_user_groups",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="custom_user_permissions",
        related_query_name="user",
    )

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name
            else str(_("Foydalanuvchi"))
        )

    class Meta:
        verbose_name = _("Foydalanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")
        ordering = ["-created_at"]
        db_table = "users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["username"]),
        ]

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def save(self, *args, **kwargs):
        if self.avatar:
            img = Image.open(self.avatar)
            if img.format != "WEBP":
                img_io = io.BytesIO()
                img.save(img_io, format="WEBP")
                self.avatar.save(
                    f"{self.avatar.name.split('.')[0]}.webp",
                    ContentFile(img_io.getvalue()),
                    save=False,
                )
        super().save(*args, **kwargs)
