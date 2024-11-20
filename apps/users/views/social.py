from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from apps.users.services.github import Github
from apps.users.services.google import Google


class SocialAuthView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]

    def post(self, request, provider_name, *args, **kwargs):
        code = request.query_params.get("code")
        if not code:
            return Response(
                {"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if provider_name == "github":
            try:
                jwt_token = Github.authenticate(code)
                return Response(jwt_token, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        elif provider_name == "google":
            try:
                jwt_token = Google.authenticate(code)
                return Response(jwt_token, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(
                {"error": "Unsupported provider"}, status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, provider_name, *args, **kwargs):
        if provider_name == "github":
            url = Github.get_auth_url()
        elif provider_name == "google":
            url = Google.get_auth_url()
        else:
            return Response(
                {"error": "Unsupported provider"}, status=status.HTTP_400_BAD_REQUEST
            )
        return HttpResponseRedirect(url)
