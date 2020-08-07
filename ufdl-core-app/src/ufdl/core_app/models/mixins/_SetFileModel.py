from typing import Optional

from django.db import models


class SetFileModel(models.Model):
    """
    Mixin model for adding the ability to set a file against
    an object.
    """
    class Meta:
        abstract = True

    def set_file(self, data: Optional[bytes]):
        """
        Sets the file for the model to the given data.

        :param data:    The file data, or None to delete the file.
        """
        raise NotImplementedError(SetFileModel.set_file.__qualname__)
