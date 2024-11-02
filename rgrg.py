from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from social_core.exceptions import NotAllowedToCreate

User = get_user_model()


class GoogleLogin(APIView):
    def post(self, request):
        # Google dan kelgan tokenni olish
        token = request.data.get("token")

        try:
            # Google orqali foydalanuvchini autentifikatsiya qilish
            user = self.authenticate_user(token)
            jwt_token = self.get_jwt(user)
            return Response(
                {"refresh": jwt_token[1], "access": jwt_token[0]},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def authenticate_user(self, token):
        # Google API orqali foydalanuvchini tekshirish
        from social_django.utils import social_auth_to_user

        # Foydalanuvchini olish
        user = social_auth_to_user(token, "google-oauth2")
        if user is None:
            raise NotAllowedToCreate
        return user

    def get_jwt(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token), str(refresh)
