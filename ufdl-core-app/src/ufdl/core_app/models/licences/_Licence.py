from django.db import models

from ...apps import UFDLCoreAppConfig


class LicenceQuerySet(models.QuerySet):
    """
    A query-set of data-set licences.
    """
    pass


class Licence(models.Model):
    """
    The licence for a data-set.
    """
    # The name for the licence
    name = models.CharField(max_length=100)

    # The URL to the licences homepage
    url = models.URLField()

    # The permissions of the licence
    permissions = models.ManyToManyField(f"{UFDLCoreAppConfig.label}.Permission",
                                         related_name="+")

    # The permissions of the licence
    limitations = models.ManyToManyField(f"{UFDLCoreAppConfig.label}.Limitation",
                                         related_name="+")

    # The permissions of the licence
    conditions = models.ManyToManyField(f"{UFDLCoreAppConfig.label}.Condition",
                                        related_name="+")

    class Meta:
        constraints = [
            # Ensure that each licence has a unique name
            models.UniqueConstraint(name="unique_licence_names",
                                    fields=["name"])
        ]
