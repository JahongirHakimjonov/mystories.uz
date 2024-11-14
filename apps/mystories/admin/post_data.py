from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.mystories.models import Tag, Theme


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ["id", "name", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]


@admin.register(Theme)
class ThemeAdmin(ModelAdmin):
    list_display = ["id", "name", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]
