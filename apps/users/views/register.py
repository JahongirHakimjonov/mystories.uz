import os

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.serializers import ActivateUserSerializer
from apps.users.serializers import RegisterSerializer
from apps.users.tasks import send_activation_email


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user, uid, token = serializer.save()
            activation_link = request.build_absolute_uri(
                reverse("activate", kwargs={"uidb64": uid, "token": token})
            )
            send_activation_email.delay(user.email, activation_link)
            return Response(
                {
                    "message": "User registered successfully. Please check your email to activate your account."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ActivateUserSerializer

    def get(self, request, uidb64, token):
        serializer = self.get_serializer(data={"uidb64": uidb64, "token": token})
        serializer.is_valid(raise_exception=True)

        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        user.is_active = True
        user.save()
        url = os.getenv("FRONTEND_URL")
        return HttpResponseRedirect(url)
