from rest_framework import serializers

from apps.shared.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "code")
        model = Country
