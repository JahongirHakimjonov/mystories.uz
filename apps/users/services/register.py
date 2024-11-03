from uuid import uuid4

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
