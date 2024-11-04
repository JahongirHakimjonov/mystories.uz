from django.urls import path

from .views import HomeView, CountryView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("country/", CountryView.as_view(), name="country"),
]
