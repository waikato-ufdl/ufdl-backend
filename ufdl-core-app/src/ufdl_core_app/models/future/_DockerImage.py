from django.db import models


class DockerImageQuerySet(models.QuerySet):
    """
    Custom query-set for models.
    """
    pass


class DockerImage(models.Model):
    objects = DockerImageQuerySet.as_manager()
