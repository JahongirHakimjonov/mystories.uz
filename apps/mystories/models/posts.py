import io

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Post(AbstractBaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"), db_index=True)
    content = models.TextField(verbose_name=_("Content"), db_index=True)
    banner = models.ImageField(upload_to="posts", verbose_name=_("Banner"))
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("Author"),
    )
    theme = models.ForeignKey(
        "Theme",
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("Theme"),
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name=_("Slug"),
        db_index=True,
        unique=True,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))
    tags = models.ManyToManyField("Tag", related_name="posts", verbose_name=_("Tags"))
    like_count = models.PositiveBigIntegerField(default=0, verbose_name=_("Like count"))
    view_count = models.PositiveBigIntegerField(default=0, verbose_name=_("View count"))
    comment_count = models.PositiveBigIntegerField(
        default=0, verbose_name=_("Comment count")
    )
    saved_count = models.PositiveBigIntegerField(
        default=0, verbose_name=_("Saved count")
    )

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ["-created_at"]
        db_table = "posts"

    def __str__(self):
        return self.title

    def increment_views(self):
        """Ko'rishlar sonini oshirish uchun metod."""
        self.view_count += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.created_at.strftime('%Y-%m-%d')}")
            unique_slug = self.slug
            num = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{num}"
                num += 1
            self.slug = unique_slug
        if self.banner:
            img = Image.open(self.banner)
            if img.format != "WEBP":
                img_io = io.BytesIO()
                img.save(img_io, format="WEBP", quality=100)
                self.banner.save(
                    f"{self.banner.name.split('.')[0]}.webp",
                    ContentFile(img_io.getvalue()),
                    save=False,
                )
        self.slug = self.slug.lower()
        super().save(*args, **kwargs)


class Like(AbstractBaseModel):
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="likes", verbose_name=_("Post")
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name=_("User")
    )

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
        unique_together = ["post", "user"]
        db_table = "likes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} {self.post}"


class Comment(AbstractBaseModel):
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Post"),
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name=_("User")
    )
    content = models.TextField(verbose_name=_("Comment text"), db_index=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]
        db_table = "comments"

    def __str__(self):
        return f"{self.user} {self.post}"


class Saved(AbstractBaseModel):
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="saves", verbose_name=_("Post")
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name=_("User")
    )

    class Meta:
        verbose_name = _("Saved post")
        verbose_name_plural = _("Saved posts")
        unique_together = ["post", "user"]
        ordering = ["-created_at"]
        db_table = "saves"

    def __str__(self):
        return f"{self.user} {self.post}"
