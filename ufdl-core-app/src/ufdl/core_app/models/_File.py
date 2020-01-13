from django.db import models
from simple_django_teams.mixins import SoftDeleteModel

from ..backend.filesystem import FileSystemBackend


class FileQuerySet(models.QuerySet):
    """
    Additional functionality for working with query-sets of disk-files.
    """
    def with_handle(self, handle: str):
        return self.filter(handle=handle)


class File(models.Model):
    """
    Model representing a file on disk. Each record relates a logical name to
    the data on disk, which is stored in a hashed directory-tree structure.
    If two or more records point to the same data, the data is only stored
    once, but can be referred to by many filenames. If different files happen
    to have the same hash-value (i.e. a hash collision), a tail is appended to
    hash-filename.
    """
    # The hash used to store the file on disk
    handle = models.CharField(max_length=FileSystemBackend.Handle.MAX_STRING_REPR_LENGTH)

    objects = FileQuerySet.as_manager()

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each dataset has a unique name/version pair for the project
            models.UniqueConstraint(name="unique_file_handles",
                                    fields=["handle"])
        ]

    def get_data(self) -> bytes:
        """
        Gets the file data from the backend.

        :return:    The file data.
        """
        # Get the file-system backend from the settings
        from ..settings import ufdl_settings
        from ..backend.filesystem import FileSystemBackend
        backend: FileSystemBackend = ufdl_settings.FILESYSTEM_BACKEND.instance()

        return backend.load(backend.Handle.from_database_string(self.handle))

    @classmethod
    def get_reference_from_backend(cls, data: bytes) -> 'File':
        """
        Stores the given data in the backend file-system and returns
        a reference to it.

        :param data:    The data to store.
        :return:        The file record.
        """
        # Get the file-system backend from the settings
        from ..settings import ufdl_settings
        from ..backend.filesystem import FileSystemBackend
        backend: FileSystemBackend = ufdl_settings.FILESYSTEM_BACKEND.instance()

        # Save the data to the file-system
        handle: FileSystemBackend.Handle = backend.save(data)

        # See if an existing handle was returned
        existing = File.objects.with_handle(handle.to_database_string())
        if len(existing) != 0:
            return existing.first()

        # Create a file reference to remember the handle
        file = File(handle=handle.to_database_string())

        # Save it
        file.save()

        return file

    def __str__(self):
        return f"DiskFile {self.handle}"
