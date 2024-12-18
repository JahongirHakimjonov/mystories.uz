from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import ActiveSessions
from apps.users.serializers import BlockSessionSerializer, ActiveSessionsSerializer
from apps.users.serializers import UpdateAvatarSerializer, UpdateUserSerializer


class UpdateAvatarView(APIView):
    serializer_class = UpdateAvatarSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.update(request.user, serializer.validated_data)
        return Response(self.serializer_class(updated_instance).data)


class UpdateUserView(APIView):
    serializer_class = UpdateUserSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.update(request.user, serializer.validated_data)
        return Response(self.serializer_class(updated_instance).data)


class BlockSessionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlockSessionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = serializer.validated_data["session_id"]

        try:
            session = ActiveSessions.objects.get(id=session_id, user=request.user)
            session.is_active = False
            session.access_token = ""
            session.refresh_token = ""
            session.save()

            return Response(
                {"message": "Session blocked successfully"}, status=status.HTTP_200_OK
            )
        except ActiveSessions.DoesNotExist:
            return Response(
                {"error": "Session not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListSessionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActiveSessionsSerializer

    @method_decorator(cache_page(60 * 5))
    def get(self, request, *args, **kwargs):
        sessions = ActiveSessions.objects.filter(user=request.user, is_active=True)
        serializer = self.serializer_class(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
