from django.contrib import admin

from .models import SearchResult, Scum, ScumShot


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    pass


class ScumShotInline(admin.StackedInline):
    model = ScumShot


@admin.register(Scum)
class ScumAdmin(admin.ModelAdmin):
    inlines = [ScumShotInline]


@admin.register(ScumShot)
class ScumShotAdmin(admin.ModelAdmin):
    pass
