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
    path("posts/<int:pk>/", PostDetailUpdateDeleteView.as_view(), name="post_detail"),
    path("theme/", ThemeApiView.as_view(), name="theme_list"),
    path("theme/<int:pk>/", TagsByThemeApiView.as_view(), name="tags_by_theme"),
    path("like/", LikeApiView.as_view(), name="like"),
    path("save/", SavedApiView.as_view(), name="save"),
    path("comment/", CommentApiView.as_view(), name="comment"),
    path("comment/<int:pk>/", CommentDeleteApiView.as_view(), name="comment_delete"),
    path("notification/", NotificationApiView.as_view(), name="notification"),
]
