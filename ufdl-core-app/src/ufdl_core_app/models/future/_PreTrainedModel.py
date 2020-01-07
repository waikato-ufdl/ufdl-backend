from ._Model import ModelQuerySet, Model


class PreTrainedModelQuerySet(ModelQuerySet):
    """
    Custom query-set for models.
    """
    pass


class PreTrainedModel(Model):
    objects = PreTrainedModelQuerySet.as_manager()
