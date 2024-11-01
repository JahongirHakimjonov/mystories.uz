THIRD_PARTY_APPS = [
    # "jazzmin",
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "modeltranslation",
    "django_ckeditor_5",
    "corsheaders",
    "rosetta",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
]

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

PROJECT_APPS = [
    "apps.shared.apps.SharedConfig",
    "apps.users.apps.UsersConfig",
    "apps.mystories.apps.MystoriesConfig",
    "apps.websocket.apps.WebsocketConfig",
]
