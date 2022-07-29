from django.db import models

from ufdl.core_app.models.mixins import (
    DeleteOnNoRemainingReferencesOnlyModel,
    DeleteOnNoRemainingReferencesOnlyQuerySet
)

from ..apps import UFDLObjectDetectionAppConfig


class DatasetToPrefixQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    TODO.
    """
    pass


class DatasetToPrefix(DeleteOnNoRemainingReferencesOnlyModel):
    """
    Model relating object-detection data-sets to the applicable prefixes.
    """
    # The dataset
    dataset = models.ForeignKey(
        f"{UFDLObjectDetectionAppConfig.label}.ObjectDetectionDataset",
        on_delete=models.DO_NOTHING,
        related_name="+"
    )

    # The prefix
    prefix = models.ForeignKey(
        f"{UFDLObjectDetectionAppConfig.label}.Prefix",
        on_delete=models.DO_NOTHING,
        related_name="+"
    )

    objects = DatasetToPrefixQuerySet.as_manager()
