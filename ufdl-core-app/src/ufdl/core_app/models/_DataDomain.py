from typing import Optional

from django.db import models

from .mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class DataDomainQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of data domains.
    """
    def for_code(self, code: str) -> Optional['DataDomain']:
        """
        Gets the data-domain with the given code.

        :param code:    The code to filter to.
        :return:        The data-domain, or None if not found.
        """
        return self.filter(name=code).first()


class DataDomain(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A data domain registered with the server.
    """
    # The domain's two-letter identifier string
    name = models.CharField(max_length=2, unique=True)

    objects = DataDomainQuerySet.as_manager()

    @classmethod
    def for_code(cls, code: str) -> Optional['DataDomain']:
        """
        Gets the data-domain with the given code.

        :param code:    The code to filter to.
        :return:        The data-domain, or None if not found.
        """
        return cls.objects.for_code(code)
