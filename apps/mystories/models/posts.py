from django.db import models
from django.db.models import Index, Func
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class CastToText(Func):
    function = "MD5"
    template = "MD5(%(expressions)s::text)"


class Post(AbstractBaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"), db_index=True)
    content = models.JSONField(verbose_name=_("Content"))
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
        indexes = [
            Index(CastToText("content"), name="content_md5_idx"),
        ]

    def __str__(self):
        return self.title

    def increment_views(self):
        """Ko'rishlar sonini oshirish uchun metod."""
        self.view_count += 1
        self.save()


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

    def save(self, *args, **kwargs):
        if self.post.comments.filter(user=self.user).count() >= 5:
            raise ValueError(
                "A user cannot write more than 5 comments on a single post."
            )
        super().save(*args, **kwargs)


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
