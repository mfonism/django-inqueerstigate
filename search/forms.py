from django import forms

from .models import SearchResult


class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchResult
        fields = ("in_shot",)
