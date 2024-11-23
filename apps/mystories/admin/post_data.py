from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.mystories.models import Tag, Theme


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ["id", "theme", "name", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]
    autocomplete_fields = ["theme"]
    list_per_page = 50


@admin.register(Theme)
class ThemeAdmin(ModelAdmin):
    list_display = ["id", "name", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]
    list_per_page = 50
