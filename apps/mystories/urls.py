from django.urls import path

from apps.mystories.views import (
    PostListCreateView,
    PostDetailUpdateDeleteView,
    ThemeApiView,
    TagsByThemeApiView,
    LikeApiView,
    SavedApiView,
    CommentApiView,
    CommentDeleteApiView,
    NotificationApiView,
)

urlpatterns = [
    path("posts/", PostListCreateView.as_view(), name="posts"),
    path("posts/<int:pk>/", PostDetailUpdateDeleteView.as_view(), name="posts-detail"),
    path("theme/", ThemeApiView.as_view(), name="theme"),
    path("theme/<int:pk>/", TagsByThemeApiView.as_view(), name="theme-detail"),
    path("like/", LikeApiView.as_view(), name="like"),
    path("save/", SavedApiView.as_view(), name="save"),
    path("comment/", CommentApiView.as_view(), name="comment"),
    path("comment/<int:pk>/", CommentDeleteApiView.as_view(), name="comment-delete"),
    path("notification/", NotificationApiView.as_view(), name="notification"),
]
