import itertools
import operator

import face_recognition

from django.shortcuts import redirect, reverse
from django.views.generic import CreateView, DetailView, FormView

from . import constants
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

    def form_invalid(self, form):

        for field_errors in form.errors.as_data().values():
            for error in field_errors:

                if error.code == constants.NO_FACE_FOUND_ERROR_CODE:
                    return redirect(reverse("no-face-found"))

                if error.code == constants.MULTIPLE_FACES_FOUND_ERROR_CODE:
                    return redirect(reverse("multiple-faces-found"))

        return super().form_invalid(form)


class NoFaceFoundResultView(FormView):
    template_name = "search/error.html"
    form_class = SearchForm
    extra_context = {"error_message": "No face was found in the image you uploaded."}


class MultipleFacesFoundResultView(FormView):
    template_name = "search/error.html"
    form_class = SearchForm
    extra_context = {
        "error_message": "Multiple faces were found in the image you uploaded."
    }


class SearchResultDetailView(DetailView):
    queryset = SearchResult.objects.prefetch_related(
        "out_scum_shots", "out_scum_shots__owner"
    ).all()
    template_name = "search/result.html"
    pk_url_kwarg = "uuid"

    def get_context_data(self, **kwargs):
        extra_context = {"search_query": {}, "search_result": []}
        extra_context["search_query"]["shot_url"] = self.object.in_shot.url
        grouped_result = itertools.groupby(
            self.object.out_scum_shots.order_by("owner").all(),
            operator.attrgetter("owner"),
        )
        extra_context["search_result"] = [
            {
                "scum": {
                    "name": owner.name,
                    "location": owner.location,
                    "external_url": owner.ext_url,
                },
                "shot_urls": [scum_shot.shot.url for scum_shot in scum_shots],
            }
            for owner, scum_shots in grouped_result
        ]
        extra_context["search_result"] = sorted(
            extra_context["search_result"], key=lambda res: -len(res["shot_urls"]),
        )
        extra_context["form"] = SearchForm()

        return super().get_context_data(**kwargs, **extra_context)
