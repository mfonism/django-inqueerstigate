from django.views.generic import CreateView, DetailView

from .forms import SearchForm
from .models import SearchResult


class SearchLandingView(CreateView):
    template_name = "search/landing.html"
    form_class = SearchForm


class SearchResultDetailView(DetailView):
    queryset = SearchResult.objects.all()
    template_name = "search/result.html"
    pk_url_kwarg = "uuid"
