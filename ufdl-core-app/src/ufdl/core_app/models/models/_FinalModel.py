from django.db import models

from ...apps import UFDLCoreAppConfig
from ._Model import ModelQuerySet, Model


class FinalModelQuerySet(ModelQuerySet):
    """
    Custom query-set for final models.
    """
    pass


class FinalModel(Model):
    """
    A model produced by a job.

    TODO: Do final models need a reference to the job that created them?
    """
    # The base model this model was built from
    # TODO: Not on documentation UML diagram
    base_model = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Domain",
                                   on_delete=models.DO_NOTHING,
                                   related_name="dependent_models")

    objects = FinalModelQuerySet.as_manager()
