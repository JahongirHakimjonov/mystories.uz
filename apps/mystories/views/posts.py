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

    def get_serializer_class(self, method):
        serializer_map = {
            "GET": PostListSerializer,
            "POST": PostSerializer,
        }
        return serializer_map.get(method)

    def get_permissions(self):
        """Set permissions dynamically based on the HTTP method."""
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Post.objects.select_related("author", "theme").prefetch_related("tags")

    def get(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer_class = self.get_serializer_class("GET")
        serializer = serializer_class(
            paginated_queryset, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Handle POST requests to create a post."""
        serializer_class = self.get_serializer_class("POST")
        serializer = serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        post = serializer.save(
            author=request.user
        )  # Ensures only authenticated users reach here
        detail_serializer = PostDetailSerializer(post, context={"request": request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class PostDetailUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_serializer_class(self, method):
        """Map HTTP methods to serializers."""
        serializer_map = {
            "GET": PostDetailSerializer,
            "PATCH": PostSerializer,
            "DELETE": None,
        }
        return serializer_map.get(method)

    def get_post(self, pk, user=None):
        """Fetch post with optional author filter."""
        queryset = Post.objects.select_related("author", "theme").prefetch_related(
            "tags"
        )
        if user:
            return get_object_or_404(queryset, pk=pk, author=user)
        return get_object_or_404(queryset, pk=pk)

    def get(self, request, pk=None):
        """Handle GET request to retrieve post details."""
        post = self.get_post(pk)
        post.increment_views()  # Increment view count directly.
        serializer_class = self.get_serializer_class("GET")
        serializer = serializer_class(post, context={"request": request})
        return Response(serializer.data)

    def patch(self, request, pk=None):
        """Handle PATCH request to update post details."""
        post = self.get_post(pk, user=request.user)
        serializer_class = self.get_serializer_class("PATCH")
        serializer = serializer_class(
            post, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response(serializer_class(post, context={"request": request}).data)

    def delete(self, request, pk=None):
        """Handle DELETE request to remove a post."""
        if not pk:
            return Response(
                {"detail": "Post ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        post = PostService.delete_post(pk, request.user)
        if not post:
            return Response(
                {"detail": "Post not found or unauthorized."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )
