from django.urls import path

from .views import SearchLandingView


urlpatterns = [
    path("", SearchLandingView.as_view(), name="search-landing"),
]
