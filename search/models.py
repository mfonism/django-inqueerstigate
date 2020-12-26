import uuid

from django.db import models
from django.utils import timezone

from cloudinary.models import CloudinaryField

from .fields import NumpyArrayField


class AbstractShrewdModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()


class SearchResult(AbstractShrewdModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    in_shot = CloudinaryField("in_shot")
    out_scum_shots = models.ManyToManyField("ScumShot", related_name="search_results")

    def __str__(self):
        return self.uuid


class ScumShot(AbstractShrewdModel):
    owner = models.ForeignKey(
        "Scum", related_name="scum_shots", on_delete=models.PROTECT
    )
    shot = CloudinaryField("scum_shot")
    encoding = NumpyArrayField()

    def __str__(self):
        return self.shot.url


class Scum(AbstractShrewdModel):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=64)
    ext_url = models.URLField(max_length=256)

    def __str__(self):
        return self.name
