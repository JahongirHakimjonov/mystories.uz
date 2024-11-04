from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.users.models import User
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
            return JsonResponse(
                {
                    "message": "User registered successfully. Please check your email to activate your account."
                },
                status=status.HTTP_201_CREATED,
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return JsonResponse(
                {"message": "User activated successfully."}, status=status.HTTP_200_OK
            )
        return JsonResponse(
            {"message": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST
        )
