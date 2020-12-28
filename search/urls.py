from django.urls import path

from .views import SearchLandingView, SearchResultDetailView


urlpatterns = [
    path("", SearchLandingView.as_view(), name="search-landing"),
    path(
        "result/<uuid:uuid>",
        SearchResultDetailView.as_view(),
        name="search-result-detail",
    ),
]
