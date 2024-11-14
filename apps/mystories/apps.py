from django.apps import AppConfig


class MystoriesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.mystories"

    def ready(self):
        import apps.mystories.signals  # noqa
