import os
from io import BytesIO

import requests
from PIL import Image
from django.core.files.base import ContentFile

from apps.users.models import RegisterTypeChoices, User, UserData
from apps.users.services.register import RegisterService


class Github:
    @staticmethod
    def authenticate(code):
        try:
            token_data = Github._fetch_token(code)
            user_info, email = Github._fetch_user_info(token_data["access_token"])
            user = Github._get_or_create_user(user_info, email)
            if user_info.get("avatar_url"):
                Github._save_user_avatar(user, user_info["avatar_url"])
            Github._update_user_data(user, user_info)
            return user.tokens()
        except (ValueError, requests.RequestException) as e:
            raise ValueError(f"Authentication failed: {str(e)}")

    @staticmethod
    def _fetch_token(code):
        response = requests.post(
            "https://github.com/login/oauth/access_token",
            json={
                "client_id": os.getenv("GITHUB_CLIENT_ID"),
                "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
                "code": code,
                "redirect_uri": os.getenv("GITHUB_REDIRECT_URI"),
            },
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _fetch_user_info(access_token):
        user_response = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"},
        )
        user_response.raise_for_status()
        user_info = user_response.json()

        email = user_info.get("email")
        if not email:
            emails_response = requests.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"token {access_token}"},
            )
            emails_response.raise_for_status()
            emails = emails_response.json()
            email = next((email["email"] for email in emails if email["primary"]), None)

        if not email:
            raise ValueError("GitHub email not found")

        return user_info, email

    @staticmethod
    def _get_or_create_user(user_info, email):
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": RegisterService.check_unique_username(user_info["login"]),
                "first_name": (
                    user_info.get("name", "").split()[0]
                    if user_info.get("name")
                    else ""
                ),
                "last_name": (
                    user_info.get("name", "").split()[-1]
                    if user_info.get("name")
                    else ""
                ),
                "is_active": True,
                "register_type": RegisterTypeChoices.GITHUB,
            },
        )
        return user

    @staticmethod
    def _save_user_avatar(user, avatar_url):
        try:
            response = requests.get(avatar_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            webp_image_io = BytesIO()
            image.save(webp_image_io, format="WEBP")
            webp_image_io.seek(0)
            user.avatar.save(
                f"{user.username}_avatar.webp",
                ContentFile(webp_image_io.read()),
                save=False,
            )
            user.save()
        except requests.RequestException as e:
            print(f"Failed to save avatar: {str(e)}")

    @staticmethod
    def _update_user_data(user, user_info):
        UserData.objects.update_or_create(
            user=user,
            defaults={
                "provider": RegisterTypeChoices.GITHUB,
                "uid": user_info["id"],
                "extra_data": user_info,
            },
        )

    @staticmethod
    def get_auth_url():
        client_id = os.getenv("GITHUB_CLIENT_ID")
        redirect_uri = os.getenv("GITHUB_REDIRECT_URI")
        scopes = "user:email"
        return f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}"
