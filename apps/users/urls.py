from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from apps.users.views import (
    RegisterView,
    ActivateUserView,
    CustomTokenObtainPairView,
    SocialAuthView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path(
        "auth/activate/<uidb64>/<token>/", ActivateUserView.as_view(), name="activate"
    ),
    path(
        "auth/api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("auth/api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "auth/<str:provider_name>/callback/",
        SocialAuthView.as_view(),
        name="social_auth",
    ),
]
