from django.db import models


class PermissionQuerySet(models.QuerySet):
    """
    A query-set of data-set licence permissions.
    """
    pass


class Permission(models.Model):
    """
    A permission that a data-set licence can grant to users of the data-set.
    """
    # The name for the licence
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            # Ensure that each permission has a unique name
            models.UniqueConstraint(name="unique_permission_names",
                                    fields=["name"])
        ]
