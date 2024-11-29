from django.db import IntegrityError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mystories.models import Theme, Tag, Like, Saved, Comment
from apps.mystories.serializers import (
    ThemeSerializer,
    TagSerializer,
    LikeSerializer,
    SavedSerializer,
    CommentSerializer,
)


class ThemeApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ThemeSerializer

    @staticmethod
    def get_queryset():
        return Theme.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagsByThemeApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def get(self, request, pk):
        tags = Tag.objects.filter(theme=pk)
        serializer = self.serializer_class(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response(
                    {"detail": "You have liked this post."},
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:
                existing_like = Like.objects.filter(
                    post=serializer.validated_data["post"], user=request.user
                ).first()
                if existing_like:
                    existing_like.delete()
                    return Response(
                        {"detail": "You have unliked this post."},
                        status=status.HTTP_200_OK,
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavedApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response(
                    {"detail": "The post has been saved successfully."},
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:
                existing_entry = Saved.objects.get(
                    user=request.user, post_id=request.data["post"]
                )
                existing_entry.delete()
                return Response(
                    {"detail": "The post has been removed from the saved list."},
                    status=status.HTTP_200_OK,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            post_id = serializer.validated_data["post"].id
            user = request.user
            comment_count = Comment.objects.filter(post_id=post_id, user=user).count()

            if comment_count >= 5:
                return Response(
                    {
                        "detail": "A user cannot write more than 5 comments on a single post."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save(user=user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    @staticmethod
    def delete(request, pk):
        comment = Comment.objects.filter(pk=pk, user=request.user).first()
        if comment:
            comment.delete()
            return Response(
                {"detail": "Comment has been deleted."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Comment not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def get(self, request, pk):
        comments = Comment.objects.filter(post=pk)
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
