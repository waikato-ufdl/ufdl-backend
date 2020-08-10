from typing import Optional, Tuple

from django.db import models

from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class HardwareQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of graphics hardware designations.
    """
    def for_compute_capability(self, capability: float) -> Optional['Hardware']:
        """
        Gets the generation that covers the given compute level,
        if it exists in the query-set.

        :param capability:  The level of compute capability.
        :return:            The generation, or None if none apply.
        """
        return self.filter(min_compute_capability__lte=capability,
                           max_compute_capability__gt=capability).first()

    def get_full_compute_range(self) -> Tuple[float, float]:
        """
        Gets the full range of known compute capabilities.

        :return:    A tuple representing [min, max) compute values.
        """
        return (
            self.aggregate(models.Min("min_compute_capability"))['min_compute_capability__min'],
            self.aggregate(models.Max("max_compute_capability"))['max_compute_capability__max']
        )


class Hardware(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A generation of graphics hardware that a node might have.
    """
    # The name of the generation of hardware
    generation = models.CharField(max_length=32)

    # The minimum compute capability of the generation of hardware
    min_compute_capability = models.FloatField()

    # The maximum compute capability of the generation of hardware
    max_compute_capability = models.FloatField()

    objects = HardwareQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each generation has a unique name
            models.UniqueConstraint(name="unique_generation_names",
                                    fields=["generation"])
        ]
