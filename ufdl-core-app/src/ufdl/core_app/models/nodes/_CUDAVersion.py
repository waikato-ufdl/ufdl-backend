from django.db import models

from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class CUDAVersionQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of CUDA versions.
    """
    pass


class CUDAVersion(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A version of the CUDA platform.
    """
    # The version number
    version = models.DecimalField(max_digits=4, decimal_places=1, unique=True)

    # The full version string
    full_version = models.CharField(max_length=16, unique=True)

    # The minimum NVidia driver version that supports this CUDA version
    min_driver_version = models.CharField(max_length=16)

    objects = CUDAVersionQuerySet.as_manager()
