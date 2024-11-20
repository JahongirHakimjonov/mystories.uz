from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.mystories.models.posts import Post, Like, Comment, Saved


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = [
        "id",
        "title",
        "author",
        "like_count",
        "view_count",
        "comment_count",
        "saved_count",
        "slug",
    ]
    search_fields = ["title", "content"]
    list_filter = ["author"]
    readonly_fields = [
        "like_count",
        "view_count",
        "comment_count",
        "saved_count",
        "slug",
        "created_at",
        "updated_at",
    ]
    autocomplete_fields = ["author", "tags", "theme"]
    list_per_page = 50


@admin.register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ["id", "post", "user"]
    search_fields = ["post", "user"]
    list_filter = ["post", "user"]
    autocomplete_fields = ["post", "user"]
    list_per_page = 50


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ["id", "post", "user", "content"]
    search_fields = ["post", "user", "content"]
    list_filter = ["post", "user"]
    autocomplete_fields = ["post", "user"]
    list_per_page = 50


@admin.register(Saved)
class SavedAdmin(ModelAdmin):
    list_display = ["id", "post", "user"]
    search_fields = ["post", "user"]
    list_filter = ["post", "user"]
    autocomplete_fields = ["post", "user"]
    list_per_page = 50
