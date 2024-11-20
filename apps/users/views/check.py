from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import CheckEmailSerializer
from apps.users.serializers import CheckUsernameSerializer

User = get_user_model()


class CheckEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CheckEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        exists = User.objects.filter(email=email).exists()
        return Response({"status": not exists})


class CheckUsernameView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CheckUsernameSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        exists = User.objects.filter(username=username).exists()
        return Response({"status": not exists})
