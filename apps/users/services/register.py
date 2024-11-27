import json
from uuid import uuid4

import requests

from apps.users.models import User


class RegisterService:
    @staticmethod
    def check_unique_username(username: str):
        username = "".join(username.split(" ")).lower()

        if not User.objects.filter(username=username).exists():
            return username
        else:
            random_username = username + str(uuid4().hex[:12])
            return RegisterService.check_unique_username(random_username)

    @staticmethod
    def get_location(ip_address: str):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            data = response.json()
            return data
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def filter_meta(meta):
        serializable_meta = {}
        for key, value in meta.items():
            try:
                json.dumps({key: value})
                serializable_meta[key] = value
            except (TypeError, ValueError):
                continue
        return serializable_meta

    @staticmethod
    def get_client_ip(request):
        """
        Extract client IP address from request metadata.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
        return ip
