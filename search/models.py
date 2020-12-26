import uuid

import face_recognition

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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
        try:
            return self.shot.url
        except AttributeError:
            return super().__str__()

    def clean(self, *args, **kwargs):
        if isinstance(self.shot, UploadedFile):
            image = face_recognition.load_image_file(self.shot)
            face_locations = face_recognition.face_locations(image)

            if len(face_locations) < 1:
                raise ValidationError({"shot": _("No human face found in shot")})
            elif len(face_locations) > 1:
                raise ValidationError(
                    {"shot": _("More than one human face found in shot")}
                )

            face_encodings = face_recognition.face_encodings(
                image, known_face_locations=face_locations, num_jitters=4
            )
            self.encoding = face_encodings[0]

        super().clean(*args, **kwargs)


class Scum(AbstractShrewdModel):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=64)
    ext_url = models.URLField(max_length=256)

    def __str__(self):
        return self.name
