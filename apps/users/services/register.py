import json
from uuid import uuid4

import requests
from django.core.exceptions import ValidationError

from apps.users.models import User


class RegisterService:
    @staticmethod
    def check_unique_username(username: str) -> str:
        """
        Check if the username is unique, and if not, generate a new unique username.
        """
        username = "".join(username.split()).lower()
        if not User.objects.filter(username=username).exists():
            return username

        # Generate a random username with a uuid suffix
        for _ in range(10):  # Attempt up to 10 times to find a unique username
            random_username = f"{username}{uuid4().hex[:12]}"
            if not User.objects.filter(username=random_username).exists():
                return random_username

        # If all attempts fail, raise an error
        raise ValidationError("Unable to generate a unique username")

    @staticmethod
    def get_location(ip_address: str) -> dict:
        """
        Get the geographical location of an IP address.
        """
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    @staticmethod
    def filter_meta(meta: dict) -> dict:
        """
        Filter request metadata to ensure all values are JSON serializable.
        """
        return {
            key: value
            for key, value in meta.items()
            if RegisterService._is_json_serializable(value)
        }

    @staticmethod
    def _is_json_serializable(value) -> bool:
        """
        Check if a value is JSON serializable.
        """
        try:
            json.dumps(value)
            return True
        except (TypeError, ValueError):
            return False

    @staticmethod
    def get_client_ip(request) -> str:
        """
        Extract client IP address from request metadata.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
        return ip
