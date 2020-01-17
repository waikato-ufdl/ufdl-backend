from django.db import models
from simple_django_teams.mixins import SoftDeleteModel

from ...apps import UFDLCoreAppConfig
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

    # The reference to the file's data
    file = models.ForeignKey(f"{UFDLCoreAppConfig.label}.File",
                             on_delete=models.DO_NOTHING,
                             related_name="+")

    objects = NamedFileQuerySet.as_manager()

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each combination of name and file is only stored once
            models.UniqueConstraint(name="unique_filename_file_pairs",
                                    fields=["name", "file"])
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
        return self.file.get_data()

    @classmethod
    def get_association(cls, filename: str, file: bytes) -> 'NamedFile':
        """
        Gets a record of the association between a filename and a file.
        Returns the existing one if it exists, otherwise creates a new one.

        :param filename:    The filename.
        :param file:        The file reference or file data.
        :return:            The association.
        """
        # If the file is the raw data, create a file reference
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

        return association
