from modeltranslation.translator import TranslationOptions, register

from apps.mystories.models import Theme, Tag


@register(Theme)
class ThemeTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ("name",)
