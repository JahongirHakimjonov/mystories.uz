from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from apps.mystories.models import Post


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(default=True)
    is_author = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "banner",
            "theme",
            "tags",
            "is_active",
            "is_author",
            "is_liked",
            "is_saved",
        )

    @extend_schema_field(serializers.BooleanField)
    def get_is_author(self, obj):
        return obj.author == self.context["request"].user

    @extend_schema_field(serializers.BooleanField)
    def get_is_liked(self, obj):
        return obj.likes.filter(user=self.context["request"].user).exists()

    @extend_schema_field(serializers.BooleanField)
    def get_is_saved(self, obj):
        return obj.saves.filter(user=self.context["request"].user).exists()

    def create(self, validated_data):
        from apps.mystories.models import Tag
        from rest_framework.exceptions import ValidationError

        raw_tags = validated_data.pop("tags", "")
        tags = []
        for tag in raw_tags.replace("[", "").replace("]", "").split(","):
            stripped_tag = tag.strip()
            if stripped_tag.isdigit():
                tag_id = int(stripped_tag)
                try:
                    tag_obj = Tag.objects.get(id=tag_id)
                    tags.append(tag_obj.id)
                except Tag.DoesNotExist:
                    raise ValidationError(f"Tag with id {tag_id} does not exist.")

        post = Post.objects.create(**validated_data)
        post.tags.add(*tags)
        return post

    def to_representation(self, instance):
        from apps.mystories.serializers import ThemeSerializer, TagSerializer

        representation = super().to_representation(instance)
        representation["theme"] = ThemeSerializer(instance.theme).data
        representation["tags"] = TagSerializer(instance.tags, many=True).data
        return representation


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "content",
            "banner",
            "like_count",
            "view_count",
            "comment_count",
            "saved_count",
            "slug",
            "created_at",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["content"] = instance.content
        return representation


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "content",
            "banner",
            "theme",
            "tags",
            "view_count",
            "comment_count",
            "saved_count",
            "slug",
            "is_active",
            "created_at",
            "updated_at",
        )

    def to_representation(self, instance):
        from apps.mystories.serializers import ThemeSerializer, TagSerializer

        representation = super().to_representation(instance)
        representation["theme"] = ThemeSerializer(instance.theme).data
        representation["tags"] = TagSerializer(instance.tags, many=True).data
        return representation
