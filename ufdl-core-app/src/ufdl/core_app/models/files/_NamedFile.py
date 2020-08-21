from typing import Union, Optional

from django.db import models

import requests

from requests_file import FileAdapter

from simple_django_teams.mixins import SoftDeleteModel

from ...apps import UFDLCoreAppConfig
from ...exceptions import BadSource
from ...util import accumulate_delete
from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet, CopyableModel


class NamedFileQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet, models.QuerySet):
    """
    Additional functionality for working with query-sets of named files.
    """
    def with_filename(self, filename: str):
        return self.filter(name__filename=filename)


class NamedFile(CopyableModel, DeleteOnNoRemainingReferencesOnlyModel, models.Model):
    """
    Model relating names to files.
    """
    # The name of the file
    name = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Filename",
                             on_delete=models.DO_NOTHING,
                             related_name="+")

    # The reference to the file's data (if resident in the backend)
    file = models.ForeignKey(f"{UFDLCoreAppConfig.label}.File",
                             on_delete=models.DO_NOTHING,
                             related_name="+",
                             null=True,
                             default=None)

    # The canonical source of the data (if doing lazy retrieval)
    canonical_source = models.CharField(max_length=256, null=True, default=None)

    objects = NamedFileQuerySet.as_manager()

    @property
    def filename(self) -> str:
        """
        Through-property to the filename
        """
        return self.name.filename

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each combination of name and file is only stored once
            models.UniqueConstraint(name="unique_filename_file_pairs",
                                    fields=["name", "file"],
                                    condition=models.Q(canonical_source__isnull=True)),
            models.UniqueConstraint(name="unique_filename_file_pairs_2",
                                    fields=["name", "canonical_source"],
                                    condition=models.Q(canonical_source__isnull=False))
        ]

    def has_same_contents_as(self, other: 'NamedFile') -> bool:
        """
        Whether this file has identical contents to another.

        :param other:   The other file to compare to.
        :return:        True if the file contents are the same.
        """
        # Both files must have data to compare
        if self.file is None:
            self._load_data_from_canonical_source()
        if other.file is None:
            other._load_data_from_canonical_source()

        return self.file == other.file

    def delete(self, using=None, keep_parents=False):
        # Grab references to our filename and file
        name, file = self.name, self.file

        # Attempt to delete ourselves as usual
        deletion_accumulator = super().delete(using, keep_parents)

        # If we were deleted, delete our name and file
        if deletion_accumulator[0] == 1:
            deletion_accumulator = accumulate_delete(deletion_accumulator, name.delete())
            deletion_accumulator = accumulate_delete(deletion_accumulator, file.delete())

        return deletion_accumulator

    def get_data(self) -> bytes:
        """
        Gets the file data for this file.

        :return:    The file data.
        """
        # If the file is not resident, load it
        if self.file is None:
            self._load_data_from_canonical_source()

        return self.file.get_data()

    def _load_data_from_canonical_source(self):
        """
        Loads the file data from the specified canonical source.
        """
        # Local import to avoid circular dependency errors
        from ._File import File

        # Create a request session which can handle local files
        session = requests.Session()
        session.mount("file://", FileAdapter())

        # Download and save the file data
        try:
            self.file = File.create(session.get(self.canonical_source).content)
            self.save(update_fields=["file"])
        except Exception as e:
            raise BadSource(self.canonical_source, str(e)) from e

    @classmethod
    def create(cls, filename: str, data: Union[str, bytes, 'File']) -> 'NamedFile':
        """
        Gets a record of the association between a filename and a file. The
        file should be specified by data or canonical source. Returns the
        existing one if it exists, otherwise creates a new one.

        :param filename:    The filename.
        :param data:        The file data or canonical source.
        :return:            The association.
        """
        # Local import to avoid circularity errors
        from ._File import File

        # If the file is the raw data...
        if isinstance(data, (bytes, File)):
            # Get a reference to the data on the backend
            file = File.create(data) if isinstance(data, bytes) else data

            # Get the existing association if it exists
            association = NamedFile.objects.all().filter(name__filename=filename,
                                                         file=file).first()

            # Create a new association if it didn't exist already
            if association is None:
                # Get the filename record
                from ._Filename import Filename
                filename_record = Filename.create(filename)

                association = NamedFile(name=filename_record, file=file)
                association.save()

        # Otherwise it's a canonical source
        else:
            association = NamedFile.objects.all().filter(name__filename=filename,
                                                         canonical_source=data).first()

            # Create a new association if it didn't exist already
            if association is None:
                # Get the filename record
                from ._Filename import Filename
                filename_record = Filename.create(filename)

                association = NamedFile(name=filename_record, canonical_source=data)
                association.save()

        return association

    def copy(self, *, creator=None, new_name: Optional[str] = None, **kwargs) -> 'NamedFile':
        # Named files are unique, so if the name isn't changing, we are our own copy
        if new_name is None or new_name == self.filename:
            return self

        return self.create(new_name, self.file)
