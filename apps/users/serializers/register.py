from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password", "password_confirmation")

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirmation = attrs.get("password_confirmation")

        if password != password_confirmation:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists")
        return email

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User with this username already exists")
        return username

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        user.is_active = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return user, uid, token
