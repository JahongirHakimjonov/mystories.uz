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

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     camel_case_representation = {}
    #     for key, value in representation.items():
    #         camel_case_key = re.sub(r'_([a-z])', lambda x: x.group(1).upper(), key)
    #         camel_case_representation[camel_case_key] = value
    #     return camel_case_representation
