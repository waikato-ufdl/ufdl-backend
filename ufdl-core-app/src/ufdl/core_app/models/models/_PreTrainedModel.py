from django.db import models

from ._Model import ModelQuerySet, Model


class PreTrainedModelQuerySet(ModelQuerySet):
    """
    Custom query-set for pre-trained models.
    """
    pass


class PreTrainedModel(Model):
    """
    A pre-trained model.
    """
    # The URL of the model
    url = models.CharField(max_length=200)

    # The description of the model
    description = models.CharField(max_length=200)

    objects = PreTrainedModelQuerySet.as_manager()
