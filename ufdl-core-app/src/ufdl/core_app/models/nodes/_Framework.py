from django.db import models

from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class FrameworkQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of deep-learning frameworks.
    """
    pass


class Framework(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A deep-learning framework.
    """
    # The name of the framework
    name = models.CharField(max_length=32)

    # The version of the framework
    version = models.CharField(max_length=16)

    @property
    def name_and_version(self) -> str:
        return f"{self.name} {self.version}"

    objects = FrameworkQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each framework has a unique name/version
            models.UniqueConstraint(name="unique_frameworks",
                                    fields=["name", "version"])
        ]
