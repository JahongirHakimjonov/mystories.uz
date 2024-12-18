from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema
# from silk.profiling.profiler import silk_profile

from apps.mystories.models import Post
from apps.mystories.serializers.posts import (
    PostListSerializer,
    PostDetailSerializer,
    PostSerializer,
)
from apps.mystories.services import PostService
from apps.shared.pagination import CustomPagination


class PostListCreateView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostListSerializer
        elif self.request.method == "POST":
            return PostSerializer
        return None

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Post.objects.select_related("author", "theme").prefetch_related("tags")

    # @silk_profile()
    def get(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(
            paginated_queryset, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer_class()(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        detail_serializer = PostDetailSerializer(post, context={"request": request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class PostDetailUpdateDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostDetailSerializer
        elif self.request.method == "PATCH":
            return PostSerializer
        return PostSerializer

    def get_post(self, pk, user=None):
        queryset = Post.objects.select_related("author", "theme").prefetch_related(
            "tags"
        )
        if user:
            return get_object_or_404(queryset, pk=pk, author=user)
        return get_object_or_404(queryset, pk=pk)

    # @silk_profile()
    def get(self, request, pk=None):
        post = self.get_post(pk)
        post.increment_views()
        serializer = self.get_serializer_class()(post, context={"request": request})
        return Response(serializer.data)

    @extend_schema(operation_id="post_update")
    def patch(self, request, pk=None):
        post = self.get_post(pk, user=request.user)
        serializer = self.get_serializer_class()(
            post, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response(serializer.data)

    @extend_schema(operation_id="post_delete")
    def delete(self, request, pk=None):
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
