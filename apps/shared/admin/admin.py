from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from apps.shared.models import Country

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    filter_vertical = ("permissions",)
    list_per_page = 50


@admin.register(Country)
class CountryAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id", "name", "code", "created_at", "updated_at")
    search_fields = ("name", "code")
    list_per_page = 50
