from django.http import JsonResponse
from rest_framework.views import APIView

from apps.users.serializers import UpdateAvatarSerializer, UpdateUserSerializer


class UpdateAvatarView(APIView):
    serializer_class = UpdateAvatarSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.update(request.user, serializer.validated_data)
        return JsonResponse(self.serializer_class(updated_instance).data)


class UpdateUserView(APIView):
    serializer_class = UpdateUserSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.update(request.user, serializer.validated_data)
        return JsonResponse(self.serializer_class(updated_instance).data)
