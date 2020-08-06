from django.db import models
from simple_django_teams.mixins import SoftDeleteModel, SoftDeleteQuerySet

from ...apps import UFDLCoreAppConfig


class ModelQuerySet(SoftDeleteQuerySet):
    """
    A query-set over deep-learning models.
    """
    pass


class Model(SoftDeleteModel):
    """
    A deep-learning model.

    TODO: Who owns a model? A team? A project? The server as a whole?
    """
    # The framework the model works with
    framework = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Framework",
                                  on_delete=models.DO_NOTHING,
                                  related_name="models")

    # The domain the model operates in
    domain = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Domain",
                               on_delete=models.DO_NOTHING,
                               related_name="models")

    # The licence type for this model
    licence = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Licence",
                                on_delete=models.DO_NOTHING,
                                related_name="models")

    # The data of the model
    data = models.ForeignKey(f"{UFDLCoreAppConfig.label}.FileReference",
                             on_delete=models.DO_NOTHING,
                             related_name="+")

    objects = ModelQuerySet.as_manager()
