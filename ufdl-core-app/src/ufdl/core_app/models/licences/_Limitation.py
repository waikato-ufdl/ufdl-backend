from django.db import models

from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class LimitationQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of data-set licence limitations.
    """
    pass


class Limitation(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A limitation that a data-set licence can impose on use of the data-set.
    """
    # The name of the limitation
    name = models.CharField(max_length=100)

    objects = LimitationQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each limitation has a unique name
            models.UniqueConstraint(name="unique_limitation_names",
                                    fields=["name"])
        ]
