from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "username"

    def validate(self, attrs):
        credentials = {
            "username": attrs.get(self.username_field),
            "password": attrs.get("password"),
        }

        user = authenticate(**credentials)

        if user is None or not user.is_active:
            raise serializers.ValidationError("Invalid credentials or inactive user.")

        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email

        return {
            "refresh": str(token),
            "access": str(token.access_token),
        }
