from django.db import models


class ConditionQuerySet(models.QuerySet):
    """
    A query-set of data-set licence conditions.
    """
    pass


class Condition(models.Model):
    """
    A condition that a data-set licence can impose on use of the data-set.
    """
    # The name for the licence
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            # Ensure that each condition has a unique name
            models.UniqueConstraint(name="unique_condition_names",
                                    fields=["name"])
        ]
