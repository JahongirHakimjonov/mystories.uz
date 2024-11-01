from allauth.account.signals import user_signed_up
from django.dispatch import receiver


@receiver(user_signed_up)
def populate_profile(sociallogin, **kwargs):
    user = sociallogin.user
    extra_data = sociallogin.account.extra_data

    if sociallogin.account.provider == "google":
        user.first_name = extra_data.get("given_name")
        user.last_name = extra_data.get("family_name")
        user.email = extra_data.get("email")
        user.avatar = extra_data.get("picture")

    elif sociallogin.account.provider == "github":
        user.username = extra_data.get("login")
        user.first_name = extra_data.get("name")
        user.email = extra_data.get("email")
        user.avatar = extra_data.get("avatar_url")

    user.save()
