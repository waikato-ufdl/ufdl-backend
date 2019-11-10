from django.db import models

from ..apps import APP_NAME
from ._OrganisationInferable import OrganisationInferable
from ._SoftDeleteModel import SoftDeleteModel, SoftDeleteQuerySet


class ProjectQuerySet(SoftDeleteQuerySet):
    """
    Custom query-set which handles project creation and deletion.
    """
    def pre_delete(self):
        # Local imports to prevent circular reference errors
        from ._Dataset import Dataset

        # Delete any datasets of this project
        Dataset.objects.filter(project__in=self).delete()

    def for_user(self, user):
        """
        Filters to the projects a user is allowed to see.

        :param user:    The user.
        :return:        The projects.
        """
        # Local import to avoid circular references
        from ._Organisation import Organisation

        # Un-authenticated/inactive users only have access to public datasets
        if not user.is_authenticated or not user.is_active:
            return self.none()

        # Superusers/staff can see all datasets
        if user.is_superuser or user.is_staff:
            return self.all()

        return self.filter(organisation__in=Organisation.objects.for_user(user))


class Project(OrganisationInferable, SoftDeleteModel):
    """
    Currently a project represents a related group of datasets.
    """
    # The name of the project
    name = models.CharField(max_length=200)

    # The date/time of project creation
    creation_time = models.DateTimeField(auto_now_add=True,
                                         editable=False)

    # The member that created the project
    creator = models.ForeignKey(f"{APP_NAME}.Membership",
                                on_delete=models.DO_NOTHING,
                                related_name="projects_created",
                                editable=False)

    # The organisation the project belongs to
    organisation = models.ForeignKey(f"{APP_NAME}.Organisation",
                                     on_delete=models.DO_NOTHING,
                                     related_name="projects")

    # Use the custom query-set manager
    objects = ProjectQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each active project has a unique name within a single organisation
            models.UniqueConstraint(name="unique_active_project_names_per_organisation",
                                    fields=["name", "organisation"],
                                    condition=SoftDeleteModel.active_Q)
        ]

    def pre_delete(self):
        self.datasets.all().delete()

    def infer_organisation(self):
        return self.organisation

    def __str__(self):
        return f"Project \"{self.name}\": {self.organisation.name}"
