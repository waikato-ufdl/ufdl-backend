from django.db import models
from simple_django_teams.mixins import SoftDeleteModel, SoftDeleteQuerySet

from ...apps import UFDLCoreAppConfig
from ...util import QueryParameterValue
from ..mixins import AsFileModel


class JobOutputQuerySet(SoftDeleteQuerySet):
    """
    A query-set over job outputs.
    """
    def with_name(self, name: str) -> 'JobOutputQuerySet':
        """
        Filters the query-set to those outputs with a certain name.

        :param name:    The name.
        :return:        The filtered query-set.
        """
        return self.filter(name=name)

    def with_type(self, type: str) -> 'JobOutputQuerySet':
        """
        Filters the query-set to those outputs with a certain type.

        :param type:    The type.
        :return:        The filtered query-set.
        """
        return self.filter(type=type)

    def with_signature(self, name: str, type: str) -> 'JobOutputQuerySet':
        """
        Filters the query-set to those outputs with a certain name and type.

        :param name:    The name.
        :param type:    The type.
        :return:        The filtered query-set.
        """
        return self.filter(name=name, type=type)


class JobOutput(AsFileModel, SoftDeleteModel):
    """
    An output from a job.
    """
    # The job which created this output
    job = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Job",
                            on_delete=models.DO_NOTHING,
                            related_name="outputs")

    # The name of the output
    name = models.CharField(max_length=200)

    # The type of output
    type = models.TextField(blank=True, default="")

    # The output data
    data = models.ForeignKey(f"{UFDLCoreAppConfig.label}.File",
                             on_delete=models.DO_NOTHING,
                             related_name="+")

    @property
    def signature(self) -> str:
        return f"{self.name} : {self.type}"

    objects = JobOutputQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each output is distinct for a given job
            models.UniqueConstraint(name="unique_job_outputs",
                                    fields=["job", "name", "type"])
        ]

    def supports_file_format(self, file_format: str):
        return True

    def default_format(self) -> str:
        return self.type

    def filename_without_extension(self) -> str:
        return self.name

    def as_file(self, file_format: str, **parameters: QueryParameterValue) -> bytes:
        return self.data.get_data()