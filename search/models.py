import uuid

import face_recognition

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from cloudinary.models import CloudinaryField

from . import constants, utils
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


class FaceShotMixin:
    shot_field = None
    encoding_field = None

    def get_shot_field(self):
        if self.shot_field is None:
            raise ImproperlyConfigured(
                f"Using FaceShotMixin (base class of {self.__class__.__name__})"
                f" without the 'shot_field' attribute is prohibited"
            )
        return self.shot_field

    def get_encoding_field(self):
        if self.encoding_field is None:
            raise ImproperlyConfigured(
                f"Using FaceShotMixin (base class of {self.__class__.__name__})"
                f" without the 'encoding_field' attribute is prohibited"
            )
        return self.encoding_field

    def clean(self, *args, **kwargs):
        if isinstance(getattr(self, self.get_shot_field()), UploadedFile):
            image = utils.load_image_file(
                getattr(self, self.get_shot_field())
            )
            face_locations = face_recognition.face_locations(image)

            if len(face_locations) < 1:
                raise ValidationError(
                    {
                        self.get_shot_field(): ValidationError(
                            _("No human face found in image"),
                            code=constants.NO_FACE_FOUND_ERROR_CODE,
                        )
                    }
                )
            elif len(face_locations) > 1:
                raise ValidationError(
                    {
                        self.get_shot_field(): ValidationError(
                            _("More than one human face found in image"),
                            code=constants.MULTIPLE_FACES_FOUND_ERROR_CODE,
                        )
                    }
                )

            face_encodings = face_recognition.face_encodings(
                image, known_face_locations=face_locations, num_jitters=4
            )
            setattr(self, self.get_encoding_field(), face_encodings[0])

        super().clean(*args, **kwargs)


class SearchResult(FaceShotMixin, AbstractShrewdModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    in_shot = CloudinaryField("search_shot")
    in_shot_encoding = NumpyArrayField()
    out_scum_shots = models.ManyToManyField("ScumShot", related_name="search_results")

    shot_field = "in_shot"
    encoding_field = "in_shot_encoding"

    def __str__(self):
        return str(self.uuid)

    def get_absolute_url(self):
        return reverse("search-result-detail", kwargs={"uuid": self.uuid})


class ScumShot(FaceShotMixin, AbstractShrewdModel):
    owner = models.ForeignKey(
        "Scum", related_name="scum_shots", on_delete=models.PROTECT
    )
    shot = CloudinaryField("scum_shot")
    encoding = NumpyArrayField()

    shot_field = "shot"
    encoding_field = "encoding"

    def __str__(self):
        try:
            return f"{self.owner.name} <{self.shot.url}>"
        except AttributeError:
            return super().__str__()


class Scum(AbstractShrewdModel):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=64)
    ext_url = models.URLField(max_length=256)

    def __str__(self):
        return self.name
