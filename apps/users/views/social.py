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
        except KeyError as e:
            return Response(
                {"error": f"Missing key: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )
        except ActiveSessions.DoesNotExist:
            return Response(
                {"error": "Active session not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
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
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
