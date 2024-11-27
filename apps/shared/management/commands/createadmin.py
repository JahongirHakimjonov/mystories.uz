from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = get_user_model()
        self.create_superuser(user, "jahongir", "jahongirhakimjonov@gmail.com", "1253")
        self.create_superuser(
            user, "Jahongir", "jahongirhakimjonov@gmail.com", "20030307mart"
        )
        self.create_superuser(
            user, "998330078587", "jahongirhakimjonov@gmail.com", "20030307mart"
        )

    def create_superuser(self, user, username, email, password):
        if not user.objects.filter(username=username).exists():
            user.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {username} created successfully.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {username} already exists.")
            )
