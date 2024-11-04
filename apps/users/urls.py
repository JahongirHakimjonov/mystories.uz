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
    MeView,
    ChangePasswordView,
    CheckEmailView,
    CheckUsernameView,
    PasswordResetView,
    PasswordResetConfirmView,
    UpdateAvatarView,
    UpdateUserView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("auth/update/avatar/", UpdateAvatarView.as_view(), name="update_avatar"),
    path("auth/update/user/", UpdateUserView.as_view(), name="update_user"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("auth/check/email/", CheckEmailView.as_view(), name="check_email"),
    path("auth/check/username/", CheckUsernameView.as_view(), name="check_username"),
    path("auth/reset/password/", PasswordResetView.as_view(), name="reset_password"),
    path(
        "auth/reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="reset_password_confirm",
    ),
    path(
        "auth/activate/<uidb64>/<token>/", ActivateUserView.as_view(), name="activate"
    ),
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "auth/<str:provider_name>/callback/",
        SocialAuthView.as_view(),
        name="social_auth",
    ),
]
