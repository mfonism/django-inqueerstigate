from django.views.generic import FormView

from .forms import SearchForm


class SearchLandingView(FormView):
    http_method_names = ("get",)
    template_name = "search/landing.html"
    form_class = SearchForm
