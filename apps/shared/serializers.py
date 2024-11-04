from rest_framework import serializers

from apps.shared.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Country
