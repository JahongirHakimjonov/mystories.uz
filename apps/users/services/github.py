import os
from concurrent.futures import ThreadPoolExecutor

import requests
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import RegisterTypeChoices
from apps.users.services.register import RegisterService

User = get_user_model()


class Github:
    @staticmethod
    def authenticate(code):
        try:
            with ThreadPoolExecutor() as executor:
                # Exchange the code for a token
                token_future = executor.submit(
                    requests.post,
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": os.getenv("GITHUB_CLIENT_ID"),
                        "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
                        "code": code,
                        "redirect_uri": os.getenv("GITHUB_REDIRECT_URI"),
                    },
                    headers={"Accept": "application/json"},
                )
                token_response = token_future.result()
                token_response.raise_for_status()
                token_data = token_response.json()

                # Check if access_token is in the response
                if "access_token" not in token_data:
                    raise ValueError("Access token not found in the response")

                access_token = token_data["access_token"]

                # Get user info from GitHub
                user_info_future = executor.submit(
                    requests.get,
                    "https://api.github.com/user",
                    headers={"Authorization": f"token {access_token}"},
                )
                user_info_response = user_info_future.result()
                user_info_response.raise_for_status()
                user_info = user_info_response.json()

                # Get or create the user based on the email
                email = user_info.get("email")
                if not email:
                    # Fetch primary email if not provided in user info
                    emails_future = executor.submit(
                        requests.get,
                        "https://api.github.com/user/emails",
                        headers={"Authorization": f"token {access_token}"},
                    )
                    emails_response = emails_future.result()
                    emails_response.raise_for_status()
                    emails = emails_response.json()
                    email = next(
                        (email["email"] for email in emails if email["primary"]), None
                    )

                if not email:
                    raise ValueError("GitHub email not found")

                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        "username": RegisterService.check_unique_username(
                            user_info["login"]
                        ),
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

                if created and user_info.get("avatar_url"):
                    # Save the avatar if the user is created and the avatar is provided
                    avatar_future = executor.submit(
                        requests.get, user_info["avatar_url"]
                    )
                    avatar_response = avatar_future.result()
                    if avatar_response.status_code == 200:
                        user.avatar.save(
                            f"{user.username}_avatar.jpg",
                            ContentFile(avatar_response.content),
                            save=False,
                        )
                        user.save()

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                return {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
        except ValueError as e:
            # Handle invalid token or expired token
            raise ValueError(f"Invalid token: {str(e)}")
        except requests.RequestException as e:
            # Handle request errors
            raise ValueError(f"Failed to exchange code: {str(e)}")

    @staticmethod
    def get_auth_url():
        client_id = os.getenv("GITHUB_CLIENT_ID")
        redirect_uri = os.getenv("GITHUB_REDIRECT_URI")
        url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}"
        response = requests.get(url)
        return response.url
