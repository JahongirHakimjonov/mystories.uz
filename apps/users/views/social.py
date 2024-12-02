from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from apps.users.models import ActiveSessions
from apps.users.services import RegisterService
from apps.users.services.github import Github
from apps.users.services.google import Google


class SocialAuthView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]

    @staticmethod
    def post(request, provider_name, *args, **kwargs):
        """
        Handle OAuth authentication for supported providers.
        """
        code = request.query_params.get("code")
        if not code:
            return Response(
                {"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if provider_name == "github":
                jwt_token = Github.authenticate(code)
            elif provider_name == "google":
                jwt_token = Google.authenticate(code)
            else:
                return Response(
                    {"error": "Unsupported provider"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            ip_address = RegisterService.get_client_ip(request)
            user_agent = request.META.get("HTTP_USER_AGENT", "Unknown User Agent")
            location = RegisterService.get_location(ip_address)
            refresh_token = jwt_token.get("refresh")
            access_token = jwt_token.get("access")
            user_id = jwt_token.get("user")

            ActiveSessions.objects.create(
                user_id=user_id,
                ip=ip_address,
                user_agent=user_agent,
                location=location,
                refresh_token=refresh_token,
                access_token=access_token,
            )

            return Response(jwt_token, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def get(request, provider_name, *args, **kwargs):
        """
        Redirect to the provider's authentication URL.
        """
        try:
            if provider_name == "github":
                url = Github.get_auth_url()
            elif provider_name == "google":
                url = Google.get_auth_url()
            else:
                return Response(
                    {"error": "Unsupported provider"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return HttpResponseRedirect(url)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
