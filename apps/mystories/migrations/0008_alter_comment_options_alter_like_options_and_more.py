# Generated by Django 5.0.8 on 2024-11-14 06:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mystories", "0007_post_is_active_post_saved_count_saved"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Comment",
                "verbose_name_plural": "Comments",
            },
        ),
        migrations.AlterModelOptions(
            name="like",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Like",
                "verbose_name_plural": "Likes",
            },
        ),
        migrations.AlterModelOptions(
            name="notification",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Notification",
                "verbose_name_plural": "Notifications",
            },
        ),
        migrations.AlterModelOptions(
            name="post",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Post",
                "verbose_name_plural": "Posts",
            },
        ),
        migrations.AlterModelOptions(
            name="saved",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Saved post",
                "verbose_name_plural": "Saved posts",
            },
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Tag",
                "verbose_name_plural": "Tags",
            },
        ),
        migrations.AlterModelOptions(
            name="theme",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Theme",
                "verbose_name_plural": "Themes",
            },
        ),
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=models.TextField(db_index=True, verbose_name="Comment text"),
        ),
        migrations.AlterField(
            model_name="comment",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, verbose_name="Created at"
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="mystories.post",
                verbose_name="Post",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, db_index=True, verbose_name="Updated at"
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, verbose_name="Created at"
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="mystories.post",
                verbose_name="Post",
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, db_index=True, verbose_name="Updated at"
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, verbose_name="Created at"
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="is_read",
            field=models.BooleanField(default=False, verbose_name="Is Read"),
        ),
        migrations.AlterField(
            model_name="notification",
            name="is_send",
            field=models.BooleanField(default=False, verbose_name="Is Send"),
        ),
        migrations.AlterField(
            model_name="notification",
            name="message",
            field=models.TextField(db_index=True, verbose_name="Message"),
        ),
        migrations.AlterField(
            model_name="notification",
            name="title",
            field=models.CharField(db_index=True, max_length=255, verbose_name="Title"),
        ),
        migrations.AlterField(
            model_name="notification",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, db_index=True, verbose_name="Updated at"
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Author",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="comment_count",
            field=models.PositiveBigIntegerField(
                default=0, verbose_name="Comment count"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(db_index=True, verbose_name="Content"),
        ),
        migrations.AlterField(
            model_name="post",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, verbose_name="Created at"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="post",
            name="like_count",
            field=models.PositiveBigIntegerField(default=0, verbose_name="Like count"),
        ),
        migrations.AlterField(
            model_name="post",
            name="saved_count",
            field=models.PositiveBigIntegerField(default=0, verbose_name="Saved count"),
        ),
        migrations.AlterField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(
                related_name="posts", to="mystories.tag", verbose_name="Tags"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="theme",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to="mystories.theme",
                verbose_name="Theme",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="title",
            field=models.CharField(db_index=True, max_length=255, verbose_name="Title"),
        ),
        migrations.AlterField(
            model_name="post",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, db_index=True, verbose_name="Updated at"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="view_count",
            field=models.PositiveBigIntegerField(default=0, verbose_name="View count"),
        ),
        migrations.AlterField(
            model_name="saved",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, verbose_name="Created at"
            ),
        ),
        migrations.AlterField(
            model_name="saved",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="saves",
                to="mystories.post",
                verbose_name="Post",
            ),
        ),
        migrations.AlterField(
            model_name="saved",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, db_index=True, verbose_name="Updated at"
            ),
        ),
        migrations.AlterField(
            model_name="saved",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, verbose_name="Created at"
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(db_index=True, max_length=255, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, db_index=True, verbose_name="Updated at"
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, verbose_name="Created at"
            ),
        ),
        migrations.AlterField(
            model_name="theme",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="theme",
            name="name",
            field=models.CharField(db_index=True, max_length=255, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="theme",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, db_index=True, verbose_name="Updated at"
            ),
        ),
        migrations.AlterModelTable(
            name="comment",
            table="comments",
        ),
        migrations.AlterModelTable(
            name="like",
            table="likes",
        ),
        migrations.AlterModelTable(
            name="post",
            table="posts",
        ),
        migrations.AlterModelTable(
            name="saved",
            table="saves",
        ),
    ]
