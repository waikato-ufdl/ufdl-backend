from django.db import models

from ...apps import UFDLCoreAppConfig


class FileReferenceQuerySet(models.QuerySet):
    """
    Custom query-set for memberships.
    """
    def with_filename(self, filename: str):
        return self.filter(file__name__filename=filename)


class FileReference(models.Model):
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
