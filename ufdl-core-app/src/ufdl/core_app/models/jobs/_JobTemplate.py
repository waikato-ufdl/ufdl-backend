from django.db import models
from simple_django_teams.mixins import SoftDeleteModel, SoftDeleteQuerySet

from ...apps import UFDLCoreAppConfig


class JobTemplateQuerySet(SoftDeleteQuerySet):
    """
    A query-set over job templates.
    """
    pass


class JobTemplate(SoftDeleteModel):
    """
    A job template.

    TODO: Who owns a job template? A team? A project? The server as a whole?
    """
    # The name of the job template
    name = models.CharField(max_length=64)

    # The version of the job template
    version = models.IntegerField(default=1)

    # The scope of the job template
    scope = models.CharField(max_length=16)

    # The framework the job works with
    framework = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Framework",
                                  on_delete=models.DO_NOTHING,
                                  related_name="job_templates")

    # The domain the jobs operate in
    domain = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Domain",
                               on_delete=models.DO_NOTHING,
                               related_name="job_templates")

    # The type of the job
    type = models.ForeignKey(f"{UFDLCoreAppConfig.label}.JobType",
                             on_delete=models.DO_NOTHING,
                             related_name="job_templates")

    # The name of the job's Executor class
    executor_class = models.CharField(max_length=128)

    # The dependencies required by the job
    required_packages = models.TextField()

    # The body of the job template itself (interpreted by the Executor class)
    body = models.TextField()

    @property
    def name_and_version(self) -> str:
        return f"{self.name} v{self.version}"

    objects = JobTemplateQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each input is distinct
            models.UniqueConstraint(name="unique_active_job_templates",
                                    fields=["name", "version"],
                                    condition=SoftDeleteModel.active_Q)
        ]
