from rest_framework import serializers

from apps.mystories.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "title", "message", "banner", "is_read"]
