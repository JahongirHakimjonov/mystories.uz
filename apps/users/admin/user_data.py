from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.users.models import UserData, ActiveSessions


@admin.register(UserData)
class UserDataAdmin(ModelAdmin):
    list_display = ["id", "user", "provider", "uid"]
    autocomplete_fields = ["user"]
    search_fields = ["user__first_name", "user__last_name", "uid"]
    list_per_page = 50


@admin.register(ActiveSessions)
class ActiveSessionsAdmin(ModelAdmin):
    list_display = ["id", "user", "ip", "user_agent", "last_activity"]
    autocomplete_fields = ["user"]
    search_fields = ["user__first_name", "user__last_name", "ip"]
    readonly_fields = ["created_at", "updated_at"]
    list_filter = ["last_activity"]
    list_per_page = 50
