from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.shared.models import Country
from apps.shared.serializers import CountrySerializer


class HomeView(TemplateView):
    template_name = "index.html"

    @method_decorator(cache_page(60 * 60))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CountryView(APIView):
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

    @staticmethod
    def get_queryset():
        return Country.objects.all()

    @method_decorator(cache_page(60 * 60))
    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)
