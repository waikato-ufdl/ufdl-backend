from django.db import models

from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class JobTypeQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of job types.
    """
    pass


class JobType(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A job type registered with the server.
    """
    # The name of the job type
    name = models.CharField(max_length=64, unique=True)

    # The package of the job type
    pkg = models.CharField(max_length=64)

    # The job-type's class
    cls = models.CharField(max_length=256, unique=True)

    objects = JobTypeQuerySet.as_manager()
