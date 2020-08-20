from django.db import models

from ...apps import UFDLCoreAppConfig
from ..mixins import CopyableModel


class FileReferenceQuerySet(models.QuerySet):
    """
    Custom query-set for memberships.
    """
    def with_filename(self, filename: str):
        return self.filter(file__name__filename=filename)


class FileReference(CopyableModel, models.Model):
    # The (named) file that is referred to
    file = models.ForeignKey(f"{UFDLCoreAppConfig.label}.NamedFile",
                             on_delete=models.DO_NOTHING,
                             related_name="file_references")

    # Any meta-data to associate with the file
    metadata = models.TextField(default="", blank=True)

    objects = FileReferenceQuerySet.as_manager()

    @property
    def filename(self) -> str:
        return self.file.filename

    def delete(self, using=None, keep_parents=False):
        # Delete ourselves as normal
        super().delete(using, keep_parents)

        # Provisionally delete the name <-> file association
        self.file.delete()

    def copy(self, *, creator=None, **kwargs) -> 'FileReference':
        new_reference = FileReference(file=self.file, metadata=self.metadata)
        new_reference.save()
        return new_reference
