from rest_framework import serializers

from apps.shared.serializers import CountrySerializer
from apps.users.models import User


class UpdateAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ["avatar"]

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    country = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "country"]

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.country_id = validated_data.get("country", instance.country_id)
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            "username": instance.username,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "country": CountrySerializer(instance.country).data,
        }


class BlockSessionSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
