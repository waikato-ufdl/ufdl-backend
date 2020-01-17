from django.db import models
from simple_django_teams.mixins import SoftDeleteModel

from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class FilenameQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet, models.QuerySet):
    """
    Additional functionality for working with query-sets of file-names.
    """
    def with_filename(self, filename: str):
        return self.filter(filename=filename)


class Filename(DeleteOnNoRemainingReferencesOnlyModel, models.Model):
    """
    Model specifying names for files.
    """
    # The name of the file
    filename = models.CharField(max_length=200,
                                editable=False)

    objects = FilenameQuerySet.as_manager()

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each filename is only stored once
            models.UniqueConstraint(name="unique_filenames",
                                    fields=["filename"])
        ]

    @classmethod
    def get_filename_record(cls, filename: str) -> 'Filename':
        """
        Gets an existing record if one exists for the filename,
        otherwise creates a new one.

        :param filename:    The filename to get a record for.
        :return:            The filename record.
        """
        # Get the record for the filename
        record = Filename.objects.all().with_filename(filename).first()

        # If no record is found, create it
        if record is None:
            record = Filename(filename=filename)
            record.save()

        return record
