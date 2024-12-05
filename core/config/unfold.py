import os

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from . import unfold_navigation as navigation


def environment_callback(request):  # noqa
    """
    Callback has to return a list of two values represeting text value and the color
    type of the label displayed in top right corner.
    """
    return [os.getenv("STATUS"), "success"]  # info, danger, warning, success


UNFOLD = {
    "SITE_TITLE": "Django Default",
    "SITE_HEADER": "Django Default",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("images/django-logo.png"),
        "dark": lambda request: static("images/django-logo.png"),
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("images/django-logo.png"),
        },
    ],
    "SITE_SYMBOL": "speed",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_LANGUAGES": True,
    "ENVIRONMENT": "core.config.unfold.environment_callback",
    "LOGIN": {
        "image": lambda request: static("images/login.jpg"),
    },
    "STYLES": [
        lambda request: static("css/tailwind.css"),
    ],
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "16 185 129",
            "100": "16 185 129",
            "200": "16 185 129",
            "300": "16 185 129",
            "400": "16 185 129",
            "500": "16 185 129",
            "600": "16 185 129",
            "700": "16 185 129",
            "800": "16 185 129",
            "900": "16 185 129",
            "950": "16 185 129",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "uz": "🇺🇿",
                "ru": "🇷🇺",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": navigation.PAGES,
    },
    "TABS": [
        {
            "models": [
                "mystories.post",
                "mystories.like",
                "mystories.comment",
                "mystories.saved",
            ],
            "items": [
                {
                    "title": _("Posts"),
                    "link": reverse_lazy("admin:mystories_post_changelist"),
                },
                {
                    "title": _("Likes"),
                    "link": reverse_lazy("admin:mystories_like_changelist"),
                },
                {
                    "title": _("Comments"),
                    "link": reverse_lazy("admin:mystories_comment_changelist"),
                },
                {
                    "title": _("Saved"),
                    "link": reverse_lazy("admin:mystories_saved_changelist"),
                },
            ],
        },
    ],
}
