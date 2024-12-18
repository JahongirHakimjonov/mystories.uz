from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.models import AbstractBaseModel
from apps.users.managers import UserManager


class RoleChoices(models.TextChoices):
    ADMIN = "ADMIN", _("Admin")
    USER = "USER", _("User")
    MODERATOR = "MODERATOR", _("Moderator")


class RegisterTypeChoices(models.TextChoices):
    EMAIL = "EMAIL", _("Email")
    GOOGLE = "GOOGLE", _("Google")
    GITHUB = "GITHUB", _("Github")


class User(AbstractUser, AbstractBaseModel):
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email"),
        db_index=True,
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Username"),
        db_index=True,
    )
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, verbose_name=_("Avatar")
    )
    is_active = models.BooleanField(
        default=False,
    )
    role = models.CharField(
        choices=RoleChoices,
        max_length=20,
        default=RoleChoices.USER,
        verbose_name=_("Role"),
    )
    country = models.ForeignKey(
        "shared.Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Country"),
    )
    register_type = models.CharField(
        choices=RegisterTypeChoices,
        max_length=20,
        default=RegisterTypeChoices.EMAIL,
        verbose_name=_("Register type"),
    )
    is_private = models.BooleanField(
        default=False,
        verbose_name=_("Private"),
    )
    following_count = models.PositiveBigIntegerField(
        default=0, verbose_name=_("Following count")
    )
    follower_count = models.PositiveBigIntegerField(
        default=0, verbose_name=_("Follower count")
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    def __str__(self):
        return f"{self.username} {self.email}" if self.email else str(_("User"))

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-created_at"]
        db_table = "users"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": self.id,
        }

    # def clean(self):
    #     if self.avatar and not self.avatar.storage.exists(self.avatar.name):
    #         self.avatar = None
    #
    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super().save(*args, **kwargs)


class UserData(AbstractBaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="data",
        verbose_name=_("User"),
        db_index=True,
    )
    provider = models.CharField(
        choices=RegisterTypeChoices,
        max_length=20,
        verbose_name=_("Provider"),
        db_index=True,
    )
    uid = models.CharField(max_length=100, verbose_name=_("Provider ID"), db_index=True)
    extra_data = models.JSONField(
        verbose_name=_("Extra data"), null=True, blank=True, db_index=True
    )

    class Meta:
        verbose_name = _("User data")
        verbose_name_plural = _("User data")
        db_table = "user_data"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.username} {self.user.email}"
            if self.user.email
            else str(_("User"))
        )


class ActiveSessions(AbstractBaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sessions", verbose_name=_("User")
    )
    ip = models.GenericIPAddressField(db_index=True, verbose_name=_("IP address"))
    user_agent = models.TextField(verbose_name=_("User agent"), db_index=True)
    location = models.JSONField(verbose_name=_("Location"), null=True, blank=True)
    last_activity = models.DateTimeField(
        auto_now=True, verbose_name=_("Last activity"), db_index=True
    )
    fcm_token = models.CharField(
        max_length=255,
        verbose_name=_("FCM token"),
        null=True,
        blank=True,
        db_index=True,
    )
    refresh_token = models.TextField(verbose_name=_("Refresh token"), db_index=True)
    access_token = models.TextField(verbose_name=_("Access token"), db_index=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))
    data = models.JSONField(verbose_name=_("Data"), null=True, blank=True)

    class Meta:
        verbose_name = _("Active session")
        verbose_name_plural = _("Active sessions")
        db_table = "active_sessions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} {self.ip}" if self.user else str(_("Session"))
