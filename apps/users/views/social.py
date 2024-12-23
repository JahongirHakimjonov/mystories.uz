from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from apps.users.models import ActiveSessions
from apps.users.serializers import SocialAuthSerializer
from apps.users.services import RegisterService
from apps.users.services.github import Github
from apps.users.services.google import Google


class SocialAuthView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]
    serializer_class = SocialAuthSerializer

    def post(self, request, provider_name, *args, **kwargs):
        """
        Handle OAuth authentication for supported providers.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get("code")

        try:
            jwt_token = self.authenticate_with_provider(provider_name, code)
            self.create_active_session(request, jwt_token)
            return Response(jwt_token, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response(
                {"error": f"Missing key: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def authenticate_with_provider(self, provider_name, code):
        """
        Authenticate with the given provider name and code.
        """
        if provider_name == "github":
            return Github.authenticate(code)
        elif provider_name == "google":
            return Google.authenticate(code)
        else:
            raise ValueError("Unsupported provider")

    def create_active_session(self, request, jwt_token):
        """
        Create an active session for the authenticated user.
        """
        ip_address = RegisterService.get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "Unknown User Agent")
        location = RegisterService.get_location(ip_address)
        fcm_token = request.headers.get("FCM-Token")
        ActiveSessions.objects.create(
            user_id=jwt_token.get("user"),
            ip=ip_address,
            user_agent=user_agent,
            location=location,
            refresh_token=jwt_token.get("refresh"),
            access_token=jwt_token.get("access"),
            fcm_token=fcm_token if fcm_token else None,
        )

    @staticmethod
    def get(request, provider_name, *args, **kwargs):
        """
        Redirect to the provider's authentication URL.
        """
        try:
            url = SocialAuthView.get_auth_url(provider_name)
            return HttpResponseRedirect(url)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def get_auth_url(provider_name):
        """
        Get the authentication URL for the given provider.
        """
        if provider_name == "github":
            return Github.get_auth_url()
        elif provider_name == "google":
            return Google.get_auth_url()
        else:
            raise ValueError("Unsupported provider")
