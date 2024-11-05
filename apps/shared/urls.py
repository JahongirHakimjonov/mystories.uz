from django.urls import path

from .views import HomeView, CountryView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("api/v1/country/", CountryView.as_view(), name="country"),
]
