from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "username"

    def validate(self, attrs):
        credentials = {
            "identifier": attrs.get(self.username_field) or attrs.get("email"),
            "password": attrs.get("password"),
        }

        user = authenticate(
            username=credentials["identifier"], password=credentials["password"]
        )

        if user is None:
            user = User.objects.filter(username=credentials["identifier"]).first()
            if user:
                email = user.email
                user = authenticate(username=email, password=credentials["password"])

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return {
            "refresh": str(token),
            "access": str(token.access_token),
            "user": user.id,
        }


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs.get("refresh")

        if refresh is None:
            raise serializers.ValidationError("No refresh token provided")

        return {"refresh": refresh}
