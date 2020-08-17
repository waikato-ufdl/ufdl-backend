import os
from typing import Iterator, Union

from django.db import models

from ...apps import UFDLCoreAppConfig
from ...exceptions import BadName


class FileContainerModel(models.Model):
    """
    Mixin model for adding the ability to store files "inside"
    an object.
    """
    # The files that the objects contain
    files = models.ManyToManyField(f"{UFDLCoreAppConfig.label}.FileReference",
                                   related_name="+")

    class Meta:
        abstract = True

    def iterate_filenames(self) -> Iterator[str]:
        """
        Iterates over all filenames contained by this model.
        """
        return (file.filename for file in self.files.all())

    def add_file(self, filename: str, data: Union[bytes, str]) -> 'NamedFile':
        """
        Adds a file to the container.

        :param filename:    The filename to save the file under.
        :param data:        The file data, or a canonical source to the data.
        :return:            The file association.
        """
        # Validate the filename
        filename = self.validate_filename(filename)

        # If the filename is a directory, invent a filename for it
        if filename.endswith(os.sep):
            filename = self.generate_filename(filename)

        # Otherwise check the filename isn't already in use
        else:
            self.check_filename_not_in_use(filename)

        # Create the association between name and file
        from ..files import NamedFile
        association = NamedFile.get_association(filename, data)

        # Create a reference to the association
        from ..files import FileReference
        reference = FileReference(file=association)
        reference.save()

        # Add the reference to our files
        self.files.add(reference)

        return association

    def has_file(self, filename: str, throw: bool = False) -> bool:
        """
        Checks if the container has the a file with the given filename.

        :param filename:    The filename to check for.
        :param throw:       Whether to raise a BadName error if it doesn't exist.
        :return:            Whether the filename exists.
        """
        # Get the (possible) file reference with the given name
        file_exists = self.files.all().with_filename(filename).exists()  # TODO: Remove unnecessary? all() call

        # If the file doesn't exist, raise an error if selected
        if not file_exists and throw:
            raise BadName(filename, "Doesn't exist")

        return file_exists

    def get_file_reference(self, filename: str) -> 'FileReference':
        """
        Gets a reference to the file with the given filename
        from our files.

        :param filename:    The filename.
        :return:            The file reference.
        """
        # Get the (possible) file reference with the given name
        file = self.files.all().with_filename(filename).first()  # TODO: Remove unnecessary? all() call

        # If the file doesn't exist, raise an error
        if file is None:
            raise BadName(filename, "Doesn't exist")

        return file

    def get_named_file_record(self, filename: str) -> 'NamedFile':
        """
        Gets the file from our files with the given filename.

        :param filename:    The filename.
        :return:            The named file record.
        """
        return self.get_file_reference(filename).file

    def get_file(self, filename: str) -> bytes:
        """
        Gets the contents of a file in this container.

        :param filename:    The name of the file to get.
        :return:            The file contents.
        """
        return self.get_named_file_record(filename).get_data()

    def delete_file(self, filename: str):
        """
        Deletes a file from the container.

        :param filename:    The name of the file to delete.
        :return:            The file association.
        """
        # Get the (possible) reference to the file with the given name
        reference = self.get_file_reference(filename)

        # Delete the association
        self.files.remove(reference)

        # Delete the file (tentatively)
        reference.delete()

        return reference.file

    def get_file_metadata(self, filename: str) -> str:
        """
        Gets the meta-data associated with a file.

        :param filename:    The name of the file to get the meta-data for.
        :return:            The meta-data.
        """
        return self.get_file_reference(filename).metadata

    def set_file_metadata(self, filename: str, metadata: str):
        """
        Sets the meta-data for a file.

        :param filename:    The file to set the meta-data for.
        :return:            The meta-data.
        """
        # Get the file reference
        reference = self.get_file_reference(filename)

        # Set its meta-data
        reference.metadata = metadata
        reference.save()

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

        # If normpath removed a trailing separator, reintroduce it
        if original_filename.endswith(os.sep) and not filename.endswith(os.sep):
            filename += os.sep

        # Can't specify a relative directory outside the top-level
        if filename.startswith(".."):
            raise BadName(original_filename, f"Cannot extend beyond top-level directory (start with ..)")

        return filename

    def generate_filename(self, directory: str) -> str:
        """
        Creates a filename for the given directory which
        isn't already in use.

        :param directory:   The directory the file should be in.
        :return:            The filename.
        """
        i: int = 1
        while True:
            filename: str = directory + str(i)

            if not self.files.all().with_filename(filename).exists():
                return filename

            i += 1

    def check_filename_not_in_use(self, filename: str):
        """
        Makes sure the filename is not already in use.

        :param filename:    The filename to check.
        """
        for file in self.files.all():
            if filename == file.filename:
                raise BadName(filename, "Filename already in use")
            elif file.filename.startswith(filename + "/"):
                raise BadName(filename, "Filename is already a directory prefix")
            elif filename.startswith(file.filename + "/"):
                raise BadName(filename, "Directory prefix is already a filename")
