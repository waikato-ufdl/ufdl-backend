from django.db import models
from simple_django_teams.mixins import TeamOwnedModel, SoftDeleteModel
from simple_django_teams.models import Team


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

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each active project has a unique name within a single team
            models.UniqueConstraint(name="unique_active_project_names_per_team",
                                    fields=["name", "team"],
                                    condition=SoftDeleteModel.active_Q)
        ]

    def pre_delete(self):
        self.datasets.all().delete()

    def pre_delete_bulk(self, query_set):
        # Local imports to prevent circular reference errors
        from ._Dataset import Dataset

        # Delete any datasets of this project
        Dataset.objects.filter(project__in=query_set).delete()

    def get_owning_team(self):
        return self.team

    def __str__(self):
        return f"Project \"{self.name}\": {self.team.name}"
