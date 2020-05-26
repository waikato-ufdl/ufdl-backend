from django.db import models

from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class ConditionQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of data-set licence conditions.
    """
    pass


class Condition(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A condition that a data-set licence can impose on use of the data-set.
    """
    # The name for the licence
    name = models.CharField(max_length=100)

    objects = ConditionQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each condition has a unique name
            models.UniqueConstraint(name="unique_condition_names",
                                    fields=["name"])
        ]
