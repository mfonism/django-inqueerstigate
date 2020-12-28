import itertools

import face_recognition

from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView

from .forms import SearchForm
from .models import ScumShot, SearchResult


class SearchLandingView(CreateView):
    template_name = "search/landing.html"
    form_class = SearchForm

    def form_valid(self, form):
        self.object = form.save()
        scum_shots = list(ScumShot.objects.all())
        matches = itertools.compress(
            scum_shots,
            face_recognition.compare_faces(
                list(shot.encoding for shot in scum_shots),
                self.object.in_shot_encoding,
                tolerance=0.5,
            ),
        )
        self.object.out_scum_shots.set(matches)
        self.object.save()
        return redirect(self.get_success_url())


class SearchResultDetailView(DetailView):
    queryset = SearchResult.objects.prefetch_related("out_scum_shots").all()
    template_name = "search/result.html"
    pk_url_kwarg = "uuid"
