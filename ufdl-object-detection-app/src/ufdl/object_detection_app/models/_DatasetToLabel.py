from django.db import models

from ufdl.core_app.models.mixins import (
    DeleteOnNoRemainingReferencesOnlyModel,
    DeleteOnNoRemainingReferencesOnlyQuerySet
)

from ..apps import UFDLObjectDetectionAppConfig


class DatasetToLabelQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    TODO.
    """
    pass


class DatasetToLabel(DeleteOnNoRemainingReferencesOnlyModel):
    """
    Model relating object-detection data-sets to the applicable labels.
    """
    # The dataset
    dataset = models.ForeignKey(
        f"{UFDLObjectDetectionAppConfig.label}.ObjectDetectionDataset",
        on_delete=models.DO_NOTHING,
        related_name="+"
    )

    # The label
    label = models.ForeignKey(
        f"{UFDLObjectDetectionAppConfig.label}.Label",
        on_delete=models.DO_NOTHING,
        related_name="+"
    )

    objects = DatasetToLabelQuerySet.as_manager()
