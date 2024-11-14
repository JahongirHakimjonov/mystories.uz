from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.users.models import UserData, ActiveSessions


@admin.register(UserData)
class UserDataAdmin(ModelAdmin):
    list_display = ["id", "user", "provider", "uid"]

    search_fields = ["user__first_name", "user__last_name", "uid"]


@admin.register(ActiveSessions)
class ActiveSessionsAdmin(ModelAdmin):
    list_display = ["id", "user", "ip", "user_agent", "last_activity"]

    search_fields = ["user__first_name", "user__last_name", "ip"]

    list_filter = ["last_activity"]
