from django.db import models

from ..apps import APP_NAME
from ._Model import ModelQuerySet, Model


class FinalModelQuerySet(ModelQuerySet):
    """
    Custom query-set for models.
    """
    pass


class FinalModel(Model):
    # The base model this model was built from
    base_model = models.ForeignKey(Model,
                                   on_delete=models.DO_NOTHING,
                                   related_name="dependent_models")

    # Dataset used to train this model
    training_dataset = models.ForeignKey(f"{APP_NAME}.Dataset",
                                         on_delete=models.DO_NOTHING,
                                         related_name="dependent_models")

    objects = FinalModelQuerySet.as_manager()
