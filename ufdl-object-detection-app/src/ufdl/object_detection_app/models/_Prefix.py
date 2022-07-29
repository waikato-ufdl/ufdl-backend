from django.db import models

from ufdl.core_app.models.mixins import (
    DeleteOnNoRemainingReferencesOnlyModel,
    DeleteOnNoRemainingReferencesOnlyQuerySet
)

from ..apps import UFDLObjectDetectionAppConfig


class PrefixQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    Represents a query-set of prefixes used by object-detection data-sets.
    """
    pass


class Prefix(DeleteOnNoRemainingReferencesOnlyModel):
    """
    Represents a prefix used by object-detection data-sets.
    """
    # The data-sets using this prefix
    datasets = models.ManyToManyField(
        f"{UFDLObjectDetectionAppConfig.label}.ObjectDetectionDataset",
        related_name="prefixes",
        through=f"{UFDLObjectDetectionAppConfig.label}.DatasetToPrefix"
    )

    # The prefix
    text = models.TextField(unique=True)

    objects = PrefixQuerySet.as_manager()
