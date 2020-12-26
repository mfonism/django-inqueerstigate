from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import SearchResult, Scum, ScumShot


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    pass


class ScumShotInline(admin.StackedInline):
    model = ScumShot
    extra = 1
    readonly_fields = ("encoding",)
    fields = ("shot",)


@admin.register(Scum)
class ScumAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "get_external_url")
    fields = ("name", "location", "ext_url", "created_at", "deleted_at")
    inlines = [ScumShotInline]

    def get_external_url(self, obj):
        return mark_safe('<a href="{0}">{0}</a>'.format(obj.ext_url))

    get_external_url.short_description = "external url"


@admin.register(ScumShot)
class ScumShotAdmin(admin.ModelAdmin):
    list_display = ("owner", "get_shot_url")
    fields = ("shot", "owner", "encoding", "created_at", "deleted_at")
    readonly_fields = ("encoding",)

    def get_shot_url(self, obj):
        return mark_safe('<a href="{0}">{0}</a>'.format(obj.shot.url))

    get_shot_url.short_description = "image url"
