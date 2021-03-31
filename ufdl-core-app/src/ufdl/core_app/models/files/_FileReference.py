from typing import Optional

from django.db import models

from ...apps import UFDLCoreAppConfig
from ..mixins import CopyableModel


class FileReferenceQuerySet(models.QuerySet):
    """
    Custom query-set for memberships.
    """
    def with_filename(self, filename: str):
        return self.filter(file__name__filename=filename)

    def with_prefix(self, prefix: str):
        return self.filter(file__name__filename__startswith=prefix)

    def which_is_directory_prefix_of(self, string: str):
        return (
            self
                .annotate(prefix_test_string=models.Value(string))
                .filter(
                    prefix_test_string__startswith=models.functions.Concat(
                        models.F('file__name__filename'),
                        models.Value("/"),
                        output_field=models.CharField()
                    )
                )
        )


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

    def get_data(self) -> bytes:
        return self.file.get_data()

    def has_same_data_as(self, other: 'FileReference') -> bool:
        """
        Whether this file has identical contents to another.

        :param other:   The other file to compare to.
        :return:        True if the file contents are the same.
        """
        return self.file.has_same_data_as(other.file)

    def delete(self, using=None, keep_parents=False):
        # Delete ourselves as normal
        super().delete(using, keep_parents)

        # Provisionally delete the name <-> file association
        self.file.delete()

    def copy(self, *, creator=None, new_name: Optional[str] = None, **kwargs) -> 'FileReference':
        new_reference = FileReference(file=self.file.copy(creator=creator, new_name=new_name, **kwargs),
                                      metadata=self.metadata)
        new_reference.save()
        return new_reference
