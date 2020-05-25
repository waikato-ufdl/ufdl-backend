from django.db import models


class LimitationQuerySet(models.QuerySet):
    """
    A query-set of data-set licence limitations.
    """
    pass


class Limitation(models.Model):
    """
    A limitation that a data-set licence can impose on use of the data-set.
    """
    # The name of the limitation
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            # Ensure that each limitation has a unique name
            models.UniqueConstraint(name="unique_limitation_names",
                                    fields=["name"])
        ]
