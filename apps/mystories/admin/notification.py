from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.mystories.models import Notification


@admin.register(Notification)
class NotificationAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "title", "message", "is_read", "created_at"]
    search_fields = ["title", "message"]
    autocomplete_fields = ["user"]
    list_per_page = 50
