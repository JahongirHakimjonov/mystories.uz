from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from apps.mystories.models import Post
from apps.mystories.serializers.posts import (
    PostListSerializer,
    PostDetailSerializer,
    PostSerializer,
)
from apps.mystories.services import PostService
from apps.shared.pagination import CustomPagination


class PostListCreateView(ListCreateAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostListSerializer
        elif self.request.method == "POST":
            return PostSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Post.objects.select_related("author", "theme").prefetch_related("tags")

    @method_decorator(cache_page(60 * 5))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        detail_serializer = PostDetailSerializer(post, context={"request": request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class PostDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Post.objects.select_related("author", "theme").prefetch_related("tags")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostDetailSerializer
        return PostSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        if pk:
            return get_object_or_404(self.queryset, pk=pk, author=self.request.user)
        return None

    @extend_schema(operation_id="post_detail")
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.increment_views()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @extend_schema(operation_id="post_update")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(operation_id="post_delete")
    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if not pk:
            return Response(
                {"detail": "Post ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        post = PostService.delete_post(pk, request.user)
        if not post:
            return Response(
                {"detail": "Post not found or unauthorized."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"message": "Post deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
