from django.db import models

from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class DomainQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of licence domains.
    """
    pass


class Domain(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A domain to which a licence applies.
    """
    # The name for the licence
    name = models.CharField(max_length=100)

    objects = DomainQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each domain has a unique name
            models.UniqueConstraint(name="unique_domain_names",
                                    fields=["name"])
        ]
