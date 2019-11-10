from django.db import models

from ..apps import APP_NAME
from ._OrganisationInferable import OrganisationInferable
from ._SoftDeleteModel import SoftDeleteModel, SoftDeleteQuerySet


class DatasetQuerySet(SoftDeleteQuerySet):
    """
    Custom query-set for datasets.
    """
    def public(self):
        """
        Filters datasets down to only those that are public.
        """
        return self.filter(is_public=True)

    def for_user(self, user):
        """
        Gets all datasets that a given user has read-access to.

        :param user:    The user.
        :return:        The datasets.
        """
        # Local import to avoid circular references
        from ._Organisation import Organisation

        # Un-authenticated/inactive users only have access to public datasets
        if not user.is_authenticated or not user.is_active:
            return self.public()

        # Superusers/staff can see all datasets
        if user.is_superuser or user.is_staff:
            return self.all()

        return self.filter(models.Q(is_public=True) |
                           models.Q(project__organisation__in=Organisation.objects.for_user(user)))


class Dataset(OrganisationInferable, SoftDeleteModel):
    # The name of the dataset
    name = models.CharField(max_length=200)

    # The version of the dataset
    version = models.IntegerField(default=1)

    # The creation date/time of the dataset
    creation_time = models.DateTimeField(auto_now_add=True,
                                         editable=False)

    # The member that created the dataset
    creator = models.ForeignKey(f"{APP_NAME}.Membership",
                                on_delete=models.DO_NOTHING,
                                related_name="datasets_created",
                                editable=False)

    # The project the dataset belongs to
    project = models.ForeignKey(f"{APP_NAME}.Project",
                                on_delete=models.DO_NOTHING,
                                related_name="datasets")

    # The licence type for this dataset
    licence = models.CharField(max_length=200, default="proprietary")

    # Whether the dataset is available for public download
    is_public = models.BooleanField(default=False)

    # The tags applied to this dataset
    tags = models.TextField()

    objects = DatasetQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each dataset has a unique name/version pair for the project
            models.UniqueConstraint(name="unique_project_versions",
                                    fields=["name", "version", "project"])
        ]

    def infer_organisation(self):
        return self.project.organisation

    def __str__(self):
        return f"Dataset \"{self.name}\": {self.project}"
