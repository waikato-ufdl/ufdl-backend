from django.db import models


class JobQuerySet(models.QuerySet):
    """
    Custom query-set for models.
    """
    pass


class Job(models.Model):
    objects = JobQuerySet.as_manager()
