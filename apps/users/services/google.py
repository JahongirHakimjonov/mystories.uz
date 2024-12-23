import os
import urllib.parse
from io import BytesIO

import requests
from PIL import Image
from django.core.files.base import ContentFile
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from apps.users.models import RegisterTypeChoices, UserData, User
from apps.users.services import RegisterService


class Google:
    @staticmethod
    def authenticate(code):
        try:
            token_data = Google._fetch_token(code)
            idinfo = Google._verify_token(token_data["id_token"])
            user = Google._get_or_create_user(idinfo)
            if idinfo.get("picture"):
                Google._save_user_avatar(user, idinfo["picture"])
            Google._update_user_data(user, idinfo)
            return user.tokens()
        except (ValueError, requests.RequestException) as e:
            raise ValueError(f"Authentication failed: {str(e)}")

    @staticmethod
    def _fetch_token(code):
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            json={
                "code": code,
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
                "grant_type": "authorization_code",
            },
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _verify_token(token):
        return id_token.verify_oauth2_token(
            token, google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
        )

    @staticmethod
    def _get_or_create_user(idinfo):
        user, created = User.objects.get_or_create(
            email=idinfo["email"],
            defaults={
                "username": RegisterService.check_unique_username(
                    idinfo["email"].split("@")[0]
                ),
                "first_name": idinfo.get("given_name", ""),
                "last_name": idinfo.get("family_name", ""),
                "is_active": True,
                "register_type": RegisterTypeChoices.GOOGLE,
            },
        )
        return user

    @staticmethod
    def _save_user_avatar(user, picture_url):
        try:
            response = requests.get(picture_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            webp_image_io = BytesIO()
            image.save(webp_image_io, format="WEBP")
            webp_image_io.seek(0)

            parsed_url = urllib.parse.urlparse(picture_url)
            filename = os.path.basename(parsed_url.path)
            sanitized_filename = f"{user.username}_avatar_{filename.split('.')[0]}.webp"

            user.avatar.save(
                sanitized_filename,
                ContentFile(webp_image_io.read()),
                save=False,
            )
            user.save()
        except requests.RequestException as e:
            print(f"Failed to save avatar: {str(e)}")

    @staticmethod
    def _update_user_data(user, idinfo):
        UserData.objects.update_or_create(
            user=user,
            defaults={
                "provider": RegisterTypeChoices.GOOGLE,
                "uid": idinfo["sub"],
                "extra_data": idinfo,
            },
        )

    @staticmethod
    def get_auth_url():
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        scopes = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ]
        scope = urllib.parse.quote(" ".join(scopes))
        url = (
            f"https://accounts.google.com/o/oauth2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope}"
        )
        return url
