from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.users.models import Follower


@admin.register(Follower)
class FollowerAdmin(ModelAdmin):
    list_display = ["id", "follower", "created_at"]
    search_fields = ["follower__username"]
    list_filter = ["created_at"]
