from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
