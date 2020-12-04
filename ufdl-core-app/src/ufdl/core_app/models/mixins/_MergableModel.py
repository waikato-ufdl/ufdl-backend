from typing import Optional

from django.db import models


class MergableModel(models.Model):
    """
    Mixin model for models that can be merged together.
    """
    class Meta:
        abstract = True

    def can_merge(self, other) -> Optional[str]:
        """
        Whether the 'other' object can be merged into this one.

        :param other:
                    The other model being merged into this one.
        :return:
                    None if the merge is allowable, or a reason
                    why not.
        """
        return None

    def merge(self, other) -> 'MergableModel':
        """
        Merges the other object into this one.

        :param other:   The other model being merged into this one.
        """
        raise NotImplementedError(self.merge.__qualname__)
