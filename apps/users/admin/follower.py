from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.users.models import Follower


@admin.register(Follower)
class FollowerAdmin(ModelAdmin):
    list_display = ["id", "follower", "following", "created_at"]
    search_fields = [
        "follower__username",
        "following__username",
        "follower__email",
        "following__email",
    ]
    list_filter = ["created_at"]
    autocomplete_fields = ["follower", "following"]
    list_per_page = 50
