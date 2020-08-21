from django.db import models
from simple_django_teams.mixins import SoftDeleteModel

from ...backend.filesystem import FileSystemBackend
from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class FileQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet, models.QuerySet):
    """
    Additional functionality for working with query-sets of files.
    """
    def with_handle(self, handle: str):
        """
        Gets the subset of files with a specific handle. As
        there is a uniqueness constraint on the handle, this
        should only ever return a query-set of size 0 or 1.

        :param handle:  The handle to filter for.
        :return:        The filtered query-set.
        """
        return self.filter(handle=handle)


class File(DeleteOnNoRemainingReferencesOnlyModel, models.Model):
    """
    Model representing a file. Each record contains a logical handle to
    the data, which is stored in the file-system backend selected in the
    settings.
    """
    # The handle to the file data in the file-system backend
    handle = models.CharField(max_length=FileSystemBackend.Handle.MAX_STRING_REPR_LENGTH)

    objects = FileQuerySet.as_manager()

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each file has a unique handle
            models.UniqueConstraint(name="unique_file_handles",
                                    fields=["handle"])
        ]

    def get_data(self) -> bytes:
        """
        Gets the file data from the backend.

        :return:    The file data.
        """
        # Get the file-system backend from the settings
        from ...settings import ufdl_settings
        from ...backend.filesystem import FileSystemBackend
        backend: FileSystemBackend = ufdl_settings.FILESYSTEM_BACKEND.instance()

        return backend.load(backend.Handle.from_database_string(self.handle))

    @classmethod
    def create(cls, data: bytes) -> 'File':
        """
        Stores the given data in the backend file-system and returns
        a reference to it.

        :param data:    The data to store.
        :return:        The file record.
        """
        # Get the file-system backend from the settings
        from ...settings import ufdl_settings
        from ...backend.filesystem import FileSystemBackend
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

    def delete(self, using=None, keep_parents=False):
        # Keep a reference to our handle
        handle = self.handle

        # Delete as usual (only succeeds if there are no references to us)
        deletion_accumulator = super().delete(using, keep_parents)

        # If we were deleted, delete our data from the backend
        if deletion_accumulator[0] == 1:
            # Get the file-system backend from the settings
            from ...settings import ufdl_settings
            from ...backend.filesystem import FileSystemBackend
            backend: FileSystemBackend = ufdl_settings.FILESYSTEM_BACKEND.instance()

            # Get the backend handle
            handle = backend.Handle.from_database_string(handle)

            # Delete the file
            backend.delete(handle)

        return deletion_accumulator

    def __str__(self):
        return f"File #{self.handle}"
