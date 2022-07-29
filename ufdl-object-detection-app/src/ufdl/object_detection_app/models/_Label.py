from django.db import models

from ufdl.core_app.models.mixins import (
    DeleteOnNoRemainingReferencesOnlyModel,
    DeleteOnNoRemainingReferencesOnlyQuerySet
)

from ..apps import UFDLObjectDetectionAppConfig


class LabelQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    Represents a query-set of labels used by object-detection data-sets.
    """
    pass


class Label(DeleteOnNoRemainingReferencesOnlyModel):
    """
    Represents a label used by object-detection data-sets.
    """
    # The data-sets using this label
    datasets = models.ManyToManyField(
        f"{UFDLObjectDetectionAppConfig.label}.ObjectDetectionDataset",
        related_name="labels",
        through=f"{UFDLObjectDetectionAppConfig.label}.DatasetToLabel"
    )

    # The label
    text = models.TextField(unique=True)

    objects = LabelQuerySet.as_manager()
