from typing import Set

from django.db import models


class AsFileModel(models.Model):
    """
    Mixin model for adding the ability to get an instance of
    a model in a particular file format.
    """
    # The file formats supported by the model
    file_formats: Set[str] = set()

    class Meta:
        abstract = True

    def supports_file_format(self, file_format: str):
        """
        Whether the given file format is supported by this model.
        Default implementation checks if the format is in the
        'file_formats' set.

        :param file_format:     The format to check.
        :return:                True if the format is supported.
        """
        return file_format in self.file_formats

    def default_format(self) -> str:
        """
        Gets the default format to export if one isn't selected.

        :return:    The format string.
        """
        raise NotImplementedError(self.default_format.__qualname__)

    def filename_without_extension(self) -> str:
        """
        Gets an extension-less filename to use for the file
        representation of this model.

        :return:    The filename, sans extension.
        """
        raise NotImplementedError(self.filename_without_extension.__qualname__)

    def as_file(self, file_format: str, **parameters) -> bytes:
        """
        Returns the file representation of this model record.

        :param file_format:     The format to return the record in.
        :param parameters:      Any additional parameters supplied with the request.
        :return:                The file data.
        """
        raise NotImplementedError(self.as_file.__qualname__)
