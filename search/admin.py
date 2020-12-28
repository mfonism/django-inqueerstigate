from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import SearchResult, Scum, ScumShot


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    fields = (
        "uuid",
        "get_in_shot_image",
        "get_in_shot_url",
        "in_shot_encoding",
        "out_scum_shots",
    )
    readonly_fields = (
        "uuid",
        "get_in_shot_image",
        "get_in_shot_url",
        "in_shot_encoding",
        "out_scum_shots",
    )

    def get_in_shot_url(self, obj):
        return mark_safe('<a href="{0}">{0}</a>'.format(obj.in_shot.url))

    get_in_shot_url.short_description = "inshot url"

    def get_in_shot_image(self, obj):
        print(obj.in_shot.image)
        return mark_safe(obj.in_shot.image(height=256))

    get_in_shot_image.short_description = "inshot image"


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
