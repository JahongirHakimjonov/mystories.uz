import os
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

import requests
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from apps.users.models import RegisterTypeChoices, UserData
from apps.users.services import RegisterService

User = get_user_model()


class Google:
    @staticmethod
    def authenticate(code):
        try:
            with ThreadPoolExecutor() as executor:
                # Exchange the code for a token
                token_future = executor.submit(
                    requests.post,
                    "https://oauth2.googleapis.com/token",
                    data={
                        "code": code,
                        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
                        "grant_type": "authorization_code",
                    },
                )
                token_response = token_future.result()
                token_response.raise_for_status()
                token_data = token_response.json()
                token = token_data["id_token"]

                # Verify the Google token and get user info
                idinfo = id_token.verify_oauth2_token(
                    token, google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
                )

                # Get or create the user based on the email
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

                if created and idinfo.get("picture"):
                    # Save the avatar if the user is created and the avatar is provided
                    avatar_future = executor.submit(requests.get, idinfo["picture"])
                    avatar_response = avatar_future.result()
                    if avatar_response.status_code == 200:
                        # Extract and sanitize the filename
                        parsed_url = urllib.parse.urlparse(idinfo["picture"])
                        filename = os.path.basename(parsed_url.path)
                        sanitized_filename = f"{user.username}_avatar_{filename}"

                        user.avatar.save(
                            sanitized_filename,
                            ContentFile(avatar_response.content),
                            save=False,
                        )
                        user.save()

                # Create or update UserData
                UserData.objects.update_or_create(
                    user=user,
                    defaults={
                        "provider": RegisterTypeChoices.GOOGLE,
                        "uid": idinfo["sub"],
                        "extra_data": idinfo,
                    },
                )

                # Generate JWT tokens
                token = user.tokens()
                return token
        except ValueError as e:
            # Handle invalid token or expired token
            raise ValueError(f"Invalid token: {str(e)}")
        except requests.RequestException as e:
            # Handle request errors
            raise ValueError(f"Failed to exchange code: {str(e)}")

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
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope}"
        )
        return url
