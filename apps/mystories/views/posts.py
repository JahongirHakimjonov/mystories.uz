from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from apps.mystories.models import Post
from apps.mystories.serializers.posts import (
    PostListSerializer,
    PostDetailSerializer,
    PostSerializer,
)
from apps.mystories.services import PostService
from apps.shared.pagination import CustomPagination


class PostListCreateView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]
    pagination_class = CustomPagination

    @staticmethod
    def get_queryset():
        return Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostListSerializer
        elif self.request.method in ["POST", "PATCH"]:
            return PostSerializer

    def get(self, request):
        queryset = (
            PostService.get_posts()
            .select_related("author", "theme")
            .prefetch_related("tags")
        )
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(
            paginated_queryset, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        self.permission_classes = [IsAuthenticated]
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = self.get_serializer_class()(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        return Response(PostDetailSerializer(post).data)


class PostDetailUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @staticmethod
    def get_queryset():
        return Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostDetailSerializer
        elif self.request.method in ["PATCH", "DELETE"]:
            return PostSerializer

    def get(self, request, pk=None):
        try:
            post = (
                Post.objects.select_related("author", "theme")
                .prefetch_related("tags")
                .get(pk=pk)
            )
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )
        post.increment_views()
        serializer = self.get_serializer_class()(post, context={"request": request})
        return Response(serializer.data)

    def patch(self, request, pk=None):
        self.permission_classes = [IsAuthenticated]
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        post = get_object_or_404(Post, pk=pk, author=request.user)
        serializer = self.get_serializer_class()(
            post, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response(self.get_serializer_class()(post).data)

    def delete(self, request, pk=None):
        self.permission_classes = [IsAuthenticated]
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not pk:
            return Response(
                {"detail": "Post id is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        post = PostService.delete_post(pk, request.user)
        if not post:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )
