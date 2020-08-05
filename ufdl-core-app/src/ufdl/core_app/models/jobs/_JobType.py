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
    name = models.CharField(max_length=32, unique=True)

    objects = JobTypeQuerySet.as_manager()
