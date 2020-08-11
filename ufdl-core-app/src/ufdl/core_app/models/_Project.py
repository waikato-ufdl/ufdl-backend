from django.db import models
from simple_django_teams.mixins import TeamOwnedModel, SoftDeleteModel, SoftDeleteQuerySet
from simple_django_teams.models import Team

from .mixins import UserRestrictedQuerySet


class ProjectQuerySet(UserRestrictedQuerySet, SoftDeleteQuerySet):
    """
    Custom query-set for working with groups of projects.
    """
    def for_user(self, user):
        # Users can see all projects in the teams to
        # which they are members
        from ..util import for_user
        return self.filter(
            team__in=for_user(Team.objects, user)
        )


class Project(TeamOwnedModel, SoftDeleteModel):
    """
    Currently a project represents a related group of datasets.
    """
    # The name of the project
    name = models.CharField(max_length=200)

    # The team the project belongs to
    team = models.ForeignKey(Team,
                             on_delete=models.DO_NOTHING,
                             related_name="projects")

    objects = ProjectQuerySet.as_manager()

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each active project has a unique name within a single team
            models.UniqueConstraint(name="unique_active_project_names_per_team",
                                    fields=["name", "team"],
                                    condition=SoftDeleteModel.active_Q)
        ]

    def pre_delete(self):
        self.datasets.all().delete()

    @classmethod
    def pre_delete_bulk(cls, query_set):
        # Local imports to prevent circular reference errors
        from ._Dataset import Dataset

        # Delete any datasets of this project
        Dataset.objects.filter(project__in=query_set).delete()

    def get_owning_team(self):
        return self.team

    def __str__(self):
        return f"Project \"{self.name}\": {self.team.name}"
