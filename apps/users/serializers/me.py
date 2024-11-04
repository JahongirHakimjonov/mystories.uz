from rest_framework import serializers

from apps.shared.serializers import CountrySerializer
from apps.users.models import User


class MeSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "avatar",
            "is_active",
            "role",
            "register_type",
            "country",
            "created_at",
            "updated_at",
        ]
