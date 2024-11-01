from allauth.account.admin import EmailAddressAdmin
from allauth.account.models import EmailAddress
from allauth.socialaccount.admin import (
    SocialTokenAdmin,
    SocialAccountAdmin,
)
from allauth.socialaccount.models import SocialToken, SocialApp, SocialAccount
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site
from unfold.admin import ModelAdmin

admin.site.unregister(Group)
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(Site)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_vertical = ("permissions",)


@admin.register(EmailAddress)
class EmailAddressAdmin(EmailAddressAdmin, ModelAdmin):
    list_display = ("user", "email", "verified", "primary")
    search_fields = ("user__email", "email")


@admin.register(SocialToken)
class SocialTokenAdmin(SocialTokenAdmin, ModelAdmin):
    list_display = ("app", "account", "token")
    search_fields = ("app__name", "account__user__email")


@admin.register(SocialApp)
class SocialAppAdmin(ModelAdmin):
    filter_horizontal = ("sites",)
    list_display = ("name", "provider", "client_id")


@admin.register(SocialAccount)
class SocialAccountAdmin(SocialAccountAdmin, ModelAdmin):
    list_display = ("user", "provider", "uid")
    search_fields = ("user__email", "provider", "uid")
    list_filter = ("provider",)


@admin.register(Site)
class SiteAdmin(SiteAdmin, ModelAdmin):
    pass
