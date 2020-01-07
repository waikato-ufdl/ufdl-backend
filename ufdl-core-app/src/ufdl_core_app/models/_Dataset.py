from django.db import models
from simple_django_teams.mixins import TeamOwnedModel, SoftDeleteModel, SoftDeleteQuerySet

from ..apps import APP_NAME
from .mixins import PublicModel, PublicQuerySet


class DatasetQuerySet(PublicQuerySet, SoftDeleteQuerySet):
    pass


class Dataset(TeamOwnedModel, PublicModel, SoftDeleteModel):
    # The name of the dataset
    name = models.CharField(max_length=200)

    # The version of the dataset
    version = models.IntegerField(default=1)

    # The project the dataset belongs to
    project = models.ForeignKey(f"{APP_NAME}.Project",
                                on_delete=models.DO_NOTHING,
                                related_name="datasets")

    # The licence type for this dataset
    licence = models.CharField(max_length=200, default="proprietary")

    # The tags applied to this dataset
    tags = models.TextField()

    objects = DatasetQuerySet.as_manager()

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each dataset has a unique name/version pair for the project
            models.UniqueConstraint(name="unique_datasets_per_project",
                                    fields=["name", "version", "project"])
        ]

    def get_owning_team(self):
        return self.project.team

    def __str__(self):
        return f"Dataset \"{self.name}\": {self.project}"
