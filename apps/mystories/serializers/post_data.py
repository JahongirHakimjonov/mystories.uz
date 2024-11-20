from rest_framework import serializers

from apps.mystories.models import Theme, Tag, Like, Comment, Saved


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post", "user"]
        extra_kwargs = {"user": {"read_only": True}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "user", "content"]
        extra_kwargs = {"user": {"read_only": True}}


class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved
        fields = ["id", "post", "user"]
        extra_kwargs = {"user": {"read_only": True}}
