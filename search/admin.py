from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import SearchResult, Scum, ScumShot


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ("uuid", "get_absolute_url", "get_match_count")
    fields = (
        "uuid",
        "get_absolute_url",
        "get_in_shot_image",
        "get_in_shot_url",
        "in_shot_encoding",
        "out_scum_shots",
    )
    readonly_fields = (
        "uuid",
        "get_absolute_url",
        "get_in_shot_image",
        "get_in_shot_url",
        "in_shot_encoding",
        "out_scum_shots",
    )

    def changelist_view(self, request, *args, **kwargs):
        self.request = request
        return super().changelist_view(request, *args, **kwargs)

    def get_absolute_url(self, obj):
        return mark_safe(
            '<a href="{0}">{0}</a>'.format(
                f"{'https://' if self.request.is_secure() else 'http://'}"
                f"{self.request.get_host()}"
                f"{obj.get_absolute_url()}"
            )
        )

    get_absolute_url.short_description = "absolute url"

    def get_match_count(self, obj):
        return len(set(obj.out_scum_shots.values_list("owner", flat=True)))

    get_match_count.short_description = "matches"

    def get_in_shot_url(self, obj):
        return mark_safe('<a href="{0}">{0}</a>'.format(obj.in_shot.url))

    get_in_shot_url.short_description = "inshot url"

    def get_in_shot_image(self, obj):
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
