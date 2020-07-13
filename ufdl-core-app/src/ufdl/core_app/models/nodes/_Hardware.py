from django.db import models

from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class HardwareQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of graphics hardware designations.
    """
    pass


class Hardware(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A generation of graphics hardware that a node might have.
    """
    # The name of the generation of hardware
    generation = models.CharField(max_length=32)

    # The compute capability of the generation of hardware
    compute_capability = models.CharField(max_length=8)

    objects = HardwareQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each generation has a unique name
            models.UniqueConstraint(name="unique_generation_names",
                                    fields=["generation"])
        ]
