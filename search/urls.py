from django.urls import path

from .views import (
    MultipleFacesFoundResultView,
    NoFaceFoundResultView,
    SearchLandingView,
    SearchResultDetailView,
)


urlpatterns = [
    path("", SearchLandingView.as_view(), name="search-landing"),
    path(
        "result/error/no-face-found",
        NoFaceFoundResultView.as_view(),
        name="no-face-found",
    ),
    path(
        "result/error/multiple-faces-found",
        MultipleFacesFoundResultView.as_view(),
        name="multiple-faces-found",
    ),
    path(
        "result/<uuid:uuid>",
        SearchResultDetailView.as_view(),
        name="search-result-detail",
    ),
]
