from django.db import models


class CopyableModel(models.Model):
    """
    Mixin model for adding the ability to create a new instance
    of a model by copying an existing instance.
    """
    class Meta:
        abstract = True

    def copy(self, *, creator=None, **kwargs) -> 'CopyableModel':
        """
        Creates a copy of the model.

        :param creator:     The user creating the copy.
        :return:            The copy.
        """
        raise NotImplementedError(self.copy.__qualname__)
