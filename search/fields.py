import io

import numpy as np

from django.db import models


class NumpyArrayField(models.BinaryField):
    description = "A field to save numpy arrays in the db"

    @staticmethod
    def _to_bytes(value):
        bytesIO = io.BytesIO()
        np.save(bytesIO, value)
        bytesIO.seek(0)
        return bytesIO.read()

    @staticmethod
    def _from_bytes(value):
        bytesIO = io.BytesIO(value)
        bytesIO.seek(0)
        return np.load(bytesIO)

    def get_prep_value(self, value):
        if value is None:
            return None
        return self._to_bytes(value)

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, np.ndarray):
            return value
        return self._from_bytes(value)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)
