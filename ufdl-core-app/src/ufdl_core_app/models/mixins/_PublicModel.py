from django.db import models


class PublicQuerySet(models.QuerySet):
    """
    Mixin query-set for adding publicly available support.
    """
    def public(self):
        """
        Filters datasets down to only those that are public.
        """
        return self.filter(PublicModel.public_Q)


class PublicModel(models.Model):
    """
    Mixin model for adding the ability to specify an object as
    publicly-accessible (does not require login to access).
    """
    # Whether the object is available for public access
    is_public = models.BooleanField(default=False)

    # Q object for filtering public models
    public_Q = models.Q(is_public=True)

    objects = PublicQuerySet.as_manager()

    class Meta:
        abstract = True
