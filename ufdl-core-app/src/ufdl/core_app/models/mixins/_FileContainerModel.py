import os

from django.db import models

from ...apps import UFDLCoreAppConfig
from ...exceptions import BadName


class FileContainerModel(models.Model):
    """
    Mixin model for adding the ability to store files "inside"
    an object.
    """
    # The files that the objects contain
    files = models.ManyToManyField(f"{UFDLCoreAppConfig.label}.NamedFile",
                                   related_name="+")

    class Meta:
        abstract = True

    @classmethod
    def validate_filename(cls, original_filename: str) -> str:
        """
        Validates the given filename is a valid filename
        (syntactically only). Returns the regularised version
        of the filename. This allows for logical filenames to
        include relative directory paths (so long as they don't
        go outside the top-level directory).

        :param original_filename:   The filename to validate.
        :return:                    The regularised filename.
        """
        # Collapse redundant slashes/dots
        filename = os.path.normpath(original_filename)

        # Remove any initial slashes
        while filename.startswith(os.sep):
            filename = filename[1:]

        # Can't end in a slash
        if filename.endswith(os.sep):
            raise BadName(original_filename, f"Specifies a directory (ends in {os.sep})")

        # Can't specify a relative directory outside the top-level
        if filename.startswith(".."):
            raise BadName(original_filename, f"Cannot extend beyond top-level directory (start with ..)")

        return filename

    def add_file(self, filename: str, data: bytes) -> 'NamedFile':
        """
        Adds a file to the container.

        :param filename:    The filename to save the file under.
        :param data:        The file data.
        :return:            The file association.
        """
        # Validate the filename
        filename = self.validate_filename(filename)

        # Check the filename isn't already in use
        for file in self.files.all():
            if filename == file.filename:
                raise BadName(filename, "Filename already in use")
            elif file.filename.startswith(filename + "/"):
                raise BadName(filename, "Filename is already a directory prefix")
            elif filename.startswith(file.filename + "/"):
                raise BadName(filename, "Directory prefix is already a filename")

        # Create the association between name and file
        from ..files import NamedFile
        association = NamedFile.get_association(filename, data)

        # Add the association to our files
        self.files.add(association)

        return association

    def get_file(self, filename: str) -> bytes:
        """
        Gets the contents of a file in this container.

        :param filename:    The name of the file to get.
        :return:            The file contents.
        """
        # Get the (possible) file with the given name
        file = self.files.all().with_filename(filename).first()

        # If the file doesn't exist, raise an error
        if file is None:
            raise BadName(filename, "Doesn't exist")

        return file.get_data()

    def delete_file(self, filename: str):
        """
        Deletes a file from the container.

        :param filename:    The name of the file to delete.
        :return:            The file association.
        """
        # Get the (possible) file with the given name
        file = self.files.all().with_filename(filename).first()

        # If the file doesn't exist, raise an error
        if file is None:
            raise BadName(filename, "Doesn't exist")

        # Delete the association
        self.files.remove(file)

        return file
