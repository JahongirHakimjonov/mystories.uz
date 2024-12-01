from django.core.management.base import BaseCommand

from apps.users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User
        self.create_superuser(user, "jahongir", "jahongirhakimjonov@gmail.com", "1253")

    def create_superuser(self, user, username, email, password):
        if not user.objects.filter(username=username).exists():
            user.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {username} created successfully.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {username} already exists.")
            )
