import requests
from allauth.account.signals import user_signed_up
from django.core.files.base import ContentFile
from django.dispatch import receiver

from apps.users.models import RegisterTypeChoices


@receiver(user_signed_up)
def populate_profile(sociallogin, **kwargs):
    user = sociallogin.user
    extra_data = sociallogin.account.extra_data
    avatar_url = None

    if sociallogin.account.provider == "google":
        user.first_name = extra_data.get("given_name")
        user.last_name = extra_data.get("family_name")
        user.email = extra_data.get("email")
        avatar_url = extra_data.get("picture")
        user.register_type = RegisterTypeChoices.GOOGLE
        user.is_active = True

    elif sociallogin.account.provider == "github":
        user.username = extra_data.get("login")
        user.first_name = extra_data.get("name")
        user.email = extra_data.get("email")
        avatar_url = extra_data.get("avatar_url")
        user.register_type = RegisterTypeChoices.GITHUB
        user.is_active = True

    if avatar_url:
        response = requests.get(avatar_url)
        if response.status_code == 200:
            user.avatar.save(
                f"{user.username}_avatar.jpg", ContentFile(response.content), save=False
            )

    user.save()
