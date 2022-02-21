import importlib
from typing import Type

from django.db import models

from ufdl.jobcontracts.base import UFDLJobContract

from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class JobContractQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of job contracts.
    """
    pass


class JobContract(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A job contract registered with the server.
    """
    # The name of the job contract
    name = models.CharField(max_length=64, unique=True)

    # The package of the job contract
    pkg = models.CharField(max_length=64)

    # The job-contract's class
    cls = models.CharField(max_length=256, unique=True)

    objects = JobContractQuerySet.as_manager()

    def realise_cls(self) -> Type[UFDLJobContract]:
        module_name, cls_name = self.cls.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, cls_name)
