from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def user_has_group_or_permission(user, permission):
    if user.is_superuser:
        return True

    group_names = user.groups.values_list("name", flat=True)
    if not group_names:
        return True

    return user.groups.filter(permissions__codename=permission).exists()


PAGES = [
    {
        "seperator": True,
        "items": [
            {
                "title": _("Home Page"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Users"),
        "items": [
            {
                "title": _("Groups"),
                "icon": "groups",
                "link": reverse_lazy("admin:auth_group_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Users"),
                "icon": "person_add",
                "link": reverse_lazy("admin:users_user_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Additional user data"),
        "items": [
            {
                "title": _("User Data"),
                "icon": "database",
                "link": reverse_lazy("admin:users_userdata_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_userdata"
                ),
            },
            {
                "title": _("Active Sessions"),
                "icon": "visibility_lock",
                "link": reverse_lazy("admin:users_activesessions_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_activesessions"
                ),
            },
            {
                "title": _("Followers"),
                "icon": "transfer_within_a_station",
                "link": reverse_lazy("admin:users_follower_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_follower"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Post"),
        "items": [
            {
                "title": _("Posts"),
                "icon": "post_add",
                "link": reverse_lazy("admin:mystories_post_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_post"
                ),
            },
            {
                "title": _("Post themes"),
                "icon": "menu_open",
                "link": reverse_lazy("admin:mystories_theme_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_theme"
                ),
            },
            {
                "title": _("Post tags"),
                "icon": "sell",
                "link": reverse_lazy("admin:mystories_tag_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_tag"
                ),
            },
        ],
    },
]
