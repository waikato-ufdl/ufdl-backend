from django.db import models

from .mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class DataDomainQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of data domains.
    """
    pass


class DataDomain(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A data domain registered with the server.
    """
    # The domain's two-letter identifier string
    name = models.CharField(max_length=2, unique=True)

    objects = DataDomainQuerySet.as_manager()
