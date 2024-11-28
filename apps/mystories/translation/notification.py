from modeltranslation.translator import TranslationOptions, register

from apps.mystories.models import Notification


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ("title", "message")
