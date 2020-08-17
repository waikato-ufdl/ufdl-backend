from typing import Union

from django.db import models

import requests

from requests_file import FileAdapter

from simple_django_teams.mixins import SoftDeleteModel

from ...apps import UFDLCoreAppConfig
from ...exceptions import BadSource
from ...util import accumulate_delete
from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class NamedFileQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet, models.QuerySet):
    """
    Additional functionality for working with query-sets of named files.
    """
    def with_filename(self, filename: str):
        return self.filter(name__filename=filename)


class NamedFile(DeleteOnNoRemainingReferencesOnlyModel, models.Model):
    """
    Model relating names to files.
    """
    # Through-property to the filename
    filename = property(lambda self: self.name.filename)

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
            self.file = File.get_reference_from_backend(session.get(self.canonical_source).content)
            self.save(update_fields=["file"])
        except Exception as e:
            raise BadSource(self.canonical_source, str(e)) from e

    @classmethod
    def get_association(cls, filename: str, file: Union[str, bytes]) -> 'NamedFile':
        """
        Gets a record of the association between a filename and a file. The
        file should be specified by data or canonical source. Returns the
        existing one if it exists, otherwise creates a new one.

        :param filename:    The filename.
        :param file:        The file data or canonical source.
        :return:            The association.
        """
        # If the file is the raw data...
        if isinstance(file, bytes):
            # Get a reference to the data on the backend
            from ._File import File
            file_record = File.get_reference_from_backend(file)

            # Get the existing association if it exists
            association = NamedFile.objects.all().filter(name__filename=filename,
                                                         file=file_record).first()

            # Create a new association if it didn't exist already
            if association is None:
                # Get the filename record
                from ._Filename import Filename
                filename_record = Filename.get_filename_record(filename)

                association = NamedFile(name=filename_record, file=file_record)
                association.save()

        # Otherwise it's a canonical source
        else:
            association = NamedFile.objects.all().filter(name__filename=filename,
                                                         canonical_source=file).first()

            # Create a new association if it didn't exist already
            if association is None:
                # Get the filename record
                from ._Filename import Filename
                filename_record = Filename.get_filename_record(filename)

                association = NamedFile(name=filename_record, canonical_source=file)
                association.save()

        return association
