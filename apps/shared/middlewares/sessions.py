from django.http import JsonResponse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.models import ActiveSessions
from apps.users.services import RegisterService


class CheckActiveSessionMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        """
        Middleware to check active sessions and update session information.
        """
        auth = JWTAuthentication()

        try:
            user_auth = auth.authenticate(request)
            if user_auth:
                user, token = user_auth
                fcm_token = request.headers.get("FCM-Token")
                session = ActiveSessions.objects.filter(
                    user=user, access_token=token
                ).first()
                if session:
                    session.last_activity = timezone.now()
                    session.ip_address = RegisterService.get_client_ip(request)
                    session.location = RegisterService.get_location(session.ip_address)
                    session.user_agent = request.META.get(
                        "HTTP_USER_AGENT", "Unknown User Agent"
                    )
                    if fcm_token:
                        session.fcm_token = fcm_token
                    session.save()
                    if not session.is_active:
                        return JsonResponse(
                            {"error": "Invalid access token. Session is inactive."},
                            status=status.HTTP_401_UNAUTHORIZED,
                        )
                else:
                    return JsonResponse(
                        {"error": "Session not found. Please log in again."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
        except AuthenticationFailed as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return None
