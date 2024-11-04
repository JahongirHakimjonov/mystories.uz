from rest_framework import serializers


class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CheckUsernameSerializer(serializers.Serializer):
    username = serializers.CharField()
